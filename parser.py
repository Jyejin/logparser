import gzip
import os
import csv
from models import (
    Host,
    ElbLogEntity,
    HttpRequest
)
import dataclasses
import urllib.parse, typing
import datetime

def get_log(path=os.getcwd()):
    for file in os.listdir(path):
        if file.find('.gz') != -1:
            f = gzip.open(path+file, 'rt')
            yield f.readlines()

def log_parser(logs=[]):
    fields = dataclasses.fields(ElbLogEntity)
    for log in logs:
        for row in csv.reader(log, delimiter=' '):
            yield ElbLogEntity(*
            [to_python(value, field) for value, field in zip(row, fields)])

def to_python(value, field):
    value = value.rstrip('"').lstrip('"')
    if field.type is datetime.datetime:
        return value
    if field.type == datetime.date:
        return value
    # if field.type == datetime.time:
    #     return datetime.time.fromisoformat(value)
    if field.type == typing.List[str]:
        return value.split(',')
    if value == '-':
        return None
    if field.type == Host:
        ip, port = value.split(':')
        return Host(ip, int(port))
    if field.type == HttpRequest:
        return value
    # if field.type == HttpType:
    #     return to_http_type(value)
    if field.name == 'user_agent':
        return urllib.parse.unquote(value)
    if field.name == 'uri_query':
        return urllib.parse.parse_qs(value)
    # if field.name == 'cookie':
    #     return to_cookie(value)
    return field.type(value)

def sequence(data, field, order='asc'):
    result = {}
    for d in data:
        try:
            result[d[field]] += 1
        except:
            result[d[field]] = 1
    return result

def count(data):
    return sum(1 for x in data)

def find(data, field, value):
    result = []
    for d in data:
        #todo: user_agent, client_ip등은 equal말고 regex로 찾아야 함
        if(d[field] == value):
            result.append(d)
    return result

def period(data, startdate, enddate):
    result = {}
    for d in data:
        if startdate:
            if d.time < startdate:
                continue
        if enddate:
            if d.time > enddate:
                continue
        result.append(d)
    return result