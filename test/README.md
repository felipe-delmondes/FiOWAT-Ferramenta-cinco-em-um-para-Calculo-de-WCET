Directory for unit, integration and system tests.

Inside of unit test, there are:
    - pre_generated_files: Store all files contents, whose objective is test specific situations
    - output: Store all test results


Inside of system test, there are:
    - test_01: Files and config.yaml to simulate static IPET methodology 

*Different of unit test, the system test must that the user modifies the config.yaml to your computer configuration, for example: directory, operational system, LLVM path, and so on.


All test files import "setup_test.py", to configure common setups for all files


VS Code settings for unittest:
````json
{
    "[python]": {
        "editor.defaultFormatter": "ms-python.autopep8"
    },
    "python.analysis.extraPaths": [
        "./experiments/utils",
        "./test/unit_test"
    ],
    "python.testing.unittestArgs": [
        "-v",
        "-s",
        "./test/unit_test",
        "./test/system_test",
        "-p",
        "test_*.py"
    ],
    "python.testing.pytestEnabled": false,
    "python.testing.unittestEnabled": true,
    "python.testing.autoTestDiscoverOnSaveEnabled": true
}
````