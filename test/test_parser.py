import datetime
from logparser.parser import elb_parser, count
def test_count():
    assert count == 5

def test_elb_parser(log_row):
    assert elb_parser(log_row) == ElbLogEntity(
        type='h2',
        timestamp=datetime.datetime(
        )
    )
