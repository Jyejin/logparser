import pytest
from logparser.parser import get_log

@pytest.fixture()
def log_row():
    return '''http 2020-08-01T00:00:01.183800Z app/9a5e646e4a44b708 14.42.52.187:1612 172.31.17.161:80 0.000 0.000 0.000 302 302 578 942 "GET http://123.123.123.123:80 HTTP/1.1" "Mozilla/5.0 (Windows NT 6.2; WOW64; Trident/7.0; rv:11.0) like Gecko" - - arn:aws:elasticloadbalancing:ap-northeast-2:561235816747:targetgroup/test/ea74d3a137c76d65 "Root=1-5f24b081-2e1ee6ecbc1186fedfa14aa5" "-" "-" 0 2020-08-01T00:00:01.183000Z "forward" "-" "-" "172.31.17.161:80" "302" "-" "-"'''

@pytest.fixture()
def get_test_log():
    return get_log('./logs/')