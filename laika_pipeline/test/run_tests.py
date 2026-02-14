"""Test runner that discovers and runs all test_*.py modules.

Place this file in the test package and run it to execute all
unit tests split across multiple `test_*.py` files.
"""

import os
import sys
import unittest


def main() -> None:
    loader = unittest.TestLoader()
    here = os.path.dirname(__file__)

    # Discover all test_*.py files in this directory
    suite = loader.discover(start_dir=here, pattern="test_*.py")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    # Exit non-zero on failure for CI compatibility
    sys.exit(not result.wasSuccessful())


if __name__ == "__main__":
    main()
