# Writing, running, and testing code

{% extends "_shared/contribute/how/write-code.md" %}

{% block front_matter %}

To begin working on code, ensure you have a [development environment](../how/dev-environment.md) set up, and you are [working on a branch](../how/branches.md)

{% endblock %}

{% block testing_tox_command %}

- Running the test suite on iOS

{% endblock %}

{% block testing_subset_additional %}

#### Run tests on iOS { #run-test-suite-iOS }

Rubicon ObjC also supports running on iOS. For the most part, there's no different in how Rubicon ObjC operates between macOS and iOS; but there are some subtle differences in library loading and event loop handling that sometimes require different handling.

To run the test suite on iOS:

```console
(.venv) $ tox -e py-iOS
```

{% endblock %}

{% block end_matter %}

Once you have everything working, you can [submit a pull request](../how/submit-pr.md) with your changes.

{% endblock %}
