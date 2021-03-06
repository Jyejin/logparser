import os
import gzip, csv
import datetime
import dataclasses
import multiprocessing

import urllib.parse, typing
import dateutil.parser
import pytz

from .models import (
    Host,
    ElbLogEntity,
    HttpRequest
)

def get_log(path=os.getcwd()):
    for file in os.listdir(path):
        if file.find('.gz') != -1:
            file_path = os.path.join(path, file)
            f = gzip.open(file_path, 'rt')
            yield f.readlines()

def log_parser(logs, **kwargs):
    processes = kwargs['processes'] if kwargs.get('processes') else 2
    
    p = multiprocessing.Pool(processes=processes)
    parsed_log = p.map(_log_parser, logs)
    
    result = []
    for log in parsed_log:
        result += log

    return result

def _log_parser(log):
    fields = dataclasses.fields(ElbLogEntity)
    
    parsed_log = []
    for row in csv.reader(log, delimiter=' '):
        parsed_log.append(ElbLogEntity(*
            [to_python(value, field) for value, field in zip(row, fields)]
        ))
            
    return parsed_log

def to_python(value, field):
    value = value.rstrip('"').lstrip('"')
    if field.type is datetime.datetime:
        return dateutil.parser.parse(value)
    if field.type == datetime.date:
        return dateutil.parser.parse(value)
    if field.type == typing.List[str]:
        return value.split(',')
    if value == '-':
        return None
    if field.type == Host:
        ip, port = value.split(':')
        return Host(ip, int(port))
    if field.type == HttpRequest:
        method, url, protocol = value.split(' ')
        return HttpRequest(method, url, protocol)
    if field.name == 'user_agent':
        return urllib.parse.unquote(value)
    if field.name == 'uri_query':
        return urllib.parse.parse_qs(value)
    return field.type(value)

def sequence(data, field, reverse=False):
    result = {}
    for d in data:
        try:
            result[d[field]] += 1
        except:
            result[d[field]] = 1
    return sorted(
        result.items(),
        reverse=reverse,
        key=lambda x: x[1]
    )

def count(data):
    return sum(1 for _ in data)

def find(data, field, value):
    for d in data:
        try:
            if(d[field].lower().find(value.lower()) > -1):
                yield d
        except:
            continue

def period(data, startdate=None, enddate=None):
    for d in data:
        if startdate:
            if d.time < pytz.UTC.localize(startdate):
                continue
        if enddate:
            if d.time > pytz.UTC.localize(enddate):
                continue
        yield d
