def pytest_addoption(parser):
    parser.addoption(
        "--num-trials",
        action="store",
        default=1000,
        type=int,
        help="Number of random trials to run in validation",
    )
