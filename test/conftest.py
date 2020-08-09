import pytest
from logparser.parser import get_log, log_parser

@pytest.fixture()
def get_test_log():
    return get_log('./logs/')

@pytest.fixture(scope="module")
def test_log_parse():
    return list(log_parser(get_log('./logs/')))
