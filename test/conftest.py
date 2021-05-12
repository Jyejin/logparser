import os, shutil, gzip
import pytest
from logparser.parser import get_log, log_parser

path = os.path.dirname(os.path.abspath(__file__))

http_log = '''http 2018-07-02T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 
192.168.131.39:2817 10.0.0.1:80 0.000 0.001 0.000 200 200 34 366 
"GET http://www.example.com:80/ HTTP/1.1" "curl/7.46.0" - - 
arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067 
"Root=1-58337262-36d228ad5d99923122bbe354" "-" "-" 
0 2018-07-02T22:22:48.364000Z "forward" "-" "-" 10.0.0.1:80 200 "-" "-"'''

https_log = '''https 2018-07-02T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 
192.168.131.39:2817 10.0.0.1:80 0.086 0.048 0.037 200 200 0 57 
"GET https://www.example.com:443/ HTTP/1.1" "curl/7.46.0" ECDHE-RSA-AES128-GCM-SHA256 TLSv1.2 
arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067
"Root=1-58337281-1d84f3d73c47ec4e58577259" "www.example.com" "arn:aws:acm:us-east-2:123456789012:certificate/12345678-1234-1234-1234-123456789012"
1 2018-07-02T22:22:48.364000Z "authenticate,forward" "-" "-" 10.0.0.1:80 200 "-" "-"'''

http2_log = '''h2 2018-07-02T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 
10.0.1.252:48160 10.0.0.66:9000 0.000 0.002 0.000 200 200 5 257 
"GET https://10.0.2.105:773/ HTTP/2.0" "curl/7.46.0" ECDHE-RSA-AES128-GCM-SHA256 TLSv1.2
arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067
"Root=1-58337327-72bd00b0343d75b906739c42" "-" "-"
1 2018-07-02T22:22:48.364000Z "redirect" "https://example.com:80/" "-" 10.0.0.66:9000 200 "-" "-"'''

ws_log = '''ws 2018-07-02T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 
10.0.0.140:40914 10.0.1.192:8010 0.001 0.003 0.000 101 101 218 587 
"GET http://10.0.0.30:80/ HTTP/1.1" "-" - - 
arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067
"Root=1-58337364-23a8c76965a2ef7629b185e3" "-" "-"
1 2018-07-02T22:22:48.364000Z "forward" "-" "-" 10.0.1.192:8010 101 "-" "-"'''

wss_log = '''wss 2018-07-02T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 
10.0.0.140:44244 10.0.0.171:8010 0.000 0.001 0.000 101 101 218 786
"GET https://10.0.0.30:443/ HTTP/1.1" "-" ECDHE-RSA-AES128-GCM-SHA256 TLSv1.2 
arn:aws:elasticloadbalancing:us-west-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067
"Root=1-58337364-23a8c76965a2ef7629b185e3" "-" "-"
1 2018-07-02T22:22:48.364000Z "forward" "-" "-" 10.0.0.171:8010 101 "-" "-"'''

lambda_success_log = '''http 2018-11-30T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188
192.168.131.39:2817 - 0.000 0.001 0.000 200 200 34 366
"GET http://www.example.com:80/ HTTP/1.1" "curl/7.46.0" - -
arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067
"Root=1-58337364-23a8c76965a2ef7629b185e3" "-" "-"
0 2018-11-30T22:22:48.364000Z "forward" "-" "-" "-" "-" "-" "-"'''

lambda_fail_log = '''http 2018-11-30T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188
192.168.131.39:2817 - 0.000 0.001 0.000 502 - 34 366
"GET http://www.example.com:80/ HTTP/1.1" "curl/7.46.0" - -
arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067
"Root=1-58337364-23a8c76965a2ef7629b185e3" "-" "-"
0 2018-11-30T22:22:48.364000Z "forward" "-" "LambdaInvalidResponse" "-" "-" "-" "-"''' 

def set_logdir():
    if not os.path.isdir(os.path.join(path,'logs')):
        os.mkdir(os.path.join(path,'logs'))

def set_logfile():
    logs = [http_log, https_log, http2_log, ws_log, wss_log, lambda_success_log, lambda_fail_log]
    with open(os.path.join(path,'logs','elb_log_test.log'), 'w') as f:
        for log in logs:
            f.write(log.replace('\n', ' ').replace('  ', ' ') + '\n')
    
    with open(os.path.join(path,'logs','elb_log_test.log'), 'rb') as f_in:
        with gzip.open(os.path.join(path,'logs','elb_log_test.log.gz'), 'wb') as f_out:
            f_out.writelines(f_in)

@pytest.fixture()
def get_test_log():
    return get_log('./logs')

@pytest.fixture()
def test_log_parse():
    return log_parser(get_log('./logs/'))

def pytest_runtest_setup(item):
    set_logdir()
    set_logfile()