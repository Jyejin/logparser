import datetime
from types import GeneratorType
from logparser.parser import get_log, log_parser, count, sequence, find, period

def test_get_log():
    logs = get_log('./logs/')
    assert isinstance(logs, GeneratorType)

def test_elb_parser(log_row):
    assert log_parser(log_row) == ElbLogEntity(
        type='h2',
        timestamp=datetime.datetime(
        )
    )

def test_sequence():
    pass

def test_count(get_test_log):
    assert count(get_test_log) == 50839

def test_find(get_test_log):
    find_https_type_log = find(get_test_log, 'type', 'https')
    assert len(list(find_https_type_log)) == 658
    find_Winodws_user_agent_log = find(get_test_log, 'user-agent', 'windows')
    assert len(list(find_Winodws_user_agent_log)) == 800

def test_period(get_test_log):
    #todo : 종료일 이전에 있는게 맞는지 확인, 시작일 이후에 있는게 맞는지 확인, 기간 사이에 있는게 맞는지 확인
    get_log_in_startdate = period(get_test_log,startdate=datetime.datetime.strptime('2020-08-01','%Y-%m-%d'))
    get_log_in_enddate = period(get_test_log,enddate=datetime.datetime.strptime('2020-07-31','%Y-%m-%d'))
    get_log_in_period = period(get_test_log, datetime.datetime.strptime('2020-06-30','%Y-%m-%d'),
                               datetime.datetime.strptime('2020-08-02','%Y-%m-%d'))