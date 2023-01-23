=================================
How to cut a Rubicon-ObjC release
=================================

The release infrastructure for Rubicon is semi-automated, using GitHub Actions
to formally publish releases.

This guide assumes that you have an ``upstream`` remote configured on your
local clone of the Rubicon repository, pointing at the official repository. If
all you have is a checkout of a personal fork of the Rubicon-ObjC repository,
you can configure that checkout by running::

    $ git remote add upstream https://github.com/beeware/rubicon-objc.git

The procedure for cutting a new release is as follows:

1. Check the contents of the upstream repository's main branch::

    $ git fetch upstream
    $ git checkout --detach upstream/main

   Check that the HEAD of release now matches upstream/main.

2. Ensure that the release notes are up to date. Run::

      $ tox -e towncrier -- --draft

   to review the release notes that will be included, and then::

         $ tox -e towncrier

   to generate the updated release notes.

3. Tag the release, and push the tag upstream::

    $ git tag v1.2.3
    $ git push upstream HEAD:main
    $ git push upstream v1.2.3

4. Pushing the tag will start a workflow to create a draft release on GitHub.
   You can `follow the progress of the workflow on GitHub
   <https://github.com/beeware/rubicon-objc/actions?query=workflow%3A%22Create+Release%22>`__;
   once the workflow completes, there should be a new `draft release
   <https://github.com/beeware/rubicon-objc/releases>`__, and an entry on the
   `Test PyPI server <https://test.pypi.org/project/rubicon-objc/>`__.

   Confirm that this action successfully completes. If it fails, there's a
   couple of possible causes:

   a. The final upload to Test PyPI failed. Test PyPI is not have the same
      service monitoring as PyPI-proper, so it sometimes has problems. However,
      it's also not critical to the release process; if this step fails, you can
      perform Step 6 by manually downloading the "packages" artifact from the
      GitHub workflow instead.
   b. Something else fails in the build process. If the problem can be fixed
      without a code change to the Rubicon-ObjC repository (e.g., a transient
      problem with build machines not being available), you can re-run the
      action that failed through the Github Actions GUI. If the fix requires a
      code change, delete the old tag, make the code change, and re-tag the
      release.

5. Create a clean virtual environment, install the new release from Test PyPI, and
   perform any pre-release testing that may be appropriate::

    $ python3 -m venv testvenv
    $ . ./testvenv/bin/activate
    (testvenv) $ pip install --extra-index-url https://test.pypi.org/simple/ rubicon-objc==1.2.3
    (testvenv) $ python -c "from rubicon.objc import __version__; print(__version__)"
    1.2.3
    (testvenv) $ ... any other manual checks you want to perform ...

6. Log into ReadTheDocs, visit the `Versions tab
   <https://readthedocs.org/projects/rubicon-objc/versions/>`__, and activate the
   new version. Ensure that the build completes; if there's a problem, you
   may need to correct the build configuration, roll back and re-tag the release.

7. Edit the GitHub release. Add release notes (you can use the text generated
   by towncrier). Check the pre-release checkbox (if necessary).

8. Double check everything, then click Publish. This will trigger a
   `publication workflow on GitHub
   <https://github.com/beeware/rubicon-objc/actions?query=workflow%3A%22Upload+Python+Package%22>`__.

7. Wait for the `package to appear on PyPI
<https://pypi.org/project/rubicon-objc/>`__.

Congratulations, you've just published a release!

If anything went wrong during steps 3 or 5, you will need to delete the draft
release from GitHub, and push an updated tag. Once the release has successfully
appeared on PyPI, it cannot be changed; if you spot a problem in a published
package, you'll need to tag a completely new release.
