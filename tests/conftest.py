def pytest_addoption(parser):
    parser.addoption(
        "--num-trials",
        action="store",
        default=1000,
        type=int,
        help="Number of random trials to run in validation",
    )
    parser.addoption(
        "--print-word-dict",
        action="store_true",
        default=False,
        help="Print word dictionaries",
    )
    parser.addoption(
        "--use-large-vocabulary",
        action="store_true",
        default=False,
        help="Use large vocabulary",
    )
