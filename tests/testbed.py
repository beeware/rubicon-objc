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

    # Add a short pause to make sure any log tailing gets a chance to flush. Run a
    # couple of times to make sure any log streaming dropouts don't prevent
    # Briefcase from seeing the output.
    for _ in range(6):
        print(f">>>>>>>>>> EXIT {returncode} <<<<<<<<<<")
        time.sleep(5)


if __name__ == "__main__":
    run_tests()
