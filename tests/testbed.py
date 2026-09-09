import os
import sys
import tempfile
import time
from pathlib import Path

import pytest


def run_tests():
    project_path = Path(__file__).parent.parent
    os.chdir(project_path)

    # Determine any args to pass to pytest. If there aren't any,
    # default to running the whole test suite.
    args = sys.argv[1:]
    if len(args) == 0:
        args = ["tests"]

    returncode = pytest.main(
        [
            # Turn up verbosity
            "-vv",
            # Disable color
            "--color=no",
            # Overwrite the cache directory to somewhere writable
            "-o",
            f"cache_dir={tempfile.gettempdir()}/.pytest_cache",
        ]
        + args
    )

    # Don't exit the test suite, as this causes confusion for Briefcase.
    # Keep running, and output the termination code every 5 seconds to
    # make sure it gets captured.
    while True:
        print(f">>>>>>>>>> EXIT {returncode} <<<<<<<<<<")
        time.sleep(5)


if __name__ == "__main__":
    run_tests()
