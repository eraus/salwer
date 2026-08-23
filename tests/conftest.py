def pytest_addoption(parser):
    parser.addoption(
        "--num-examples",
        action="store",
        default=1000,
        type=int,
        help="Number of examples to run in validation",
    )
