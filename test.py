# from aws_log_parser import   LogType
import dataclasses
import csv
import os
from logparser import parser
import datetime

data = parser.get_log('./test/logs/')
result = parser.log_parser(data)
# for r in result:
#     print(r['type'])
print(parser.count(result))
# for r in parser.sequence(result, 'type', reverse=True):
#     print(r)
# find_log = parser.find(result, 'type', 'https')
# print(len(list(find_log)))
# for r in parser.find(result, 'type', 'https'):
#     print(r)
# find = parser.find(result, 'user_agent', 'windows')
# for f in find:
#     print(f)
# date_log = parser.period(result, datetime.datetime.strptime('2020-06-30','%Y-%m-%d'),
#                                datetime.datetime.strptime('2020-07-31','%Y-%m-%d'))
# for r in date_log:
#     print(r['time'])

#get_log

#class parser

#find().as_data()
#find().as_csv()

