import datetime
from types import GeneratorType
from logparser.parser import get_log, log_parser, count, sequence, find, period

def test_get_log():
    logs = get_log('./logs/')
    assert isinstance(logs, GeneratorType)

def test_count(test_log_parse):
    assert count(test_log_parse) == 87060

def test_sequence(test_log_parse):
    assert sequence(test_log_parse, 'type', reverse=True) == [
        ('http', 82719),
        ('h2', 3398),
        ('https', 943)
    ]

def test_find(test_log_parse):
    find_https_type_log = find(test_log_parse, 'type', 'https')
    assert len(list(find_https_type_log)) == 943

    find_Winodws_user_agent_log = find(test_log_parse, 'user_agent', 'windows')
    assert len(list(find_Winodws_user_agent_log)) == 83049

def test_period(test_log_parse):
    get_log_after_startdate = period(test_log_parse, startdate=datetime.datetime.strptime('2020-08-01','%Y-%m-%d'))
    get_log_before_enddate = period(test_log_parse, enddate=datetime.datetime.strptime('2020-07-31','%Y-%m-%d'))
    get_log_in_period = period(test_log_parse, datetime.datetime.strptime('2020-06-30','%Y-%m-%d'),
                            datetime.datetime.strptime('2020-08-02','%Y-%m-%d'))

    assert count(get_log_after_startdate) == 32683
    assert count(get_log_before_enddate) == 21266
    assert count(get_log_in_period) == 65847
