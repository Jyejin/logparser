import datetime
from types import GeneratorType
from logparser.parser import get_log, log_parser, count, sequence, find, period

def test_get_log():
    logs = get_log('./logs/')
    assert isinstance(logs, GeneratorType)

def count1(get_test_log):
    logs = log_parser(get_test_log)
    assert count(logs) == 87060

def sequence(get_test_log):
    logs = log_parser(get_test_log)
    assert sequence(logs, 'type', reverse=True) == [
        ('http', 82719),
        ('h2', 3398),
        ('https', 943)
    ]

def find(get_test_log):
    logs = list(log_parser(get_test_log))

    find_https_type_log = find(logs, 'type', 'https')
    assert len(list(find_https_type_log)) == 943

    find_Winodws_user_agent_log = find(logs, 'user_agent', 'windows')
    assert len(list(find_Winodws_user_agent_log)) == 83049

def test_period(get_test_log):
    logs = list(log_parser(get_test_log))
    get_log_after_startdate = period(logs,startdate=datetime.datetime.strptime('2020-08-01','%Y-%m-%d'))
    get_log_before_enddate = period(logs,enddate=datetime.datetime.strptime('2020-07-31','%Y-%m-%d'))
    get_log_in_period = period(logs, datetime.datetime.strptime('2020-06-30','%Y-%m-%d'),
                               datetime.datetime.strptime('2020-08-02','%Y-%m-%d'))

    assert count(get_log_after_startdate) == 32683
    assert count(get_log_before_enddate) == 21266
    assert count(get_log_in_period) == 65847
