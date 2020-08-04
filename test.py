# from aws_log_parser import   LogType
import dataclasses
import csv
import os
import parser

data = parser.get_log('./logs/')
result = parser.log_parser(data)
for r in result:
    print(r['type'])
print(parser.count(result))
print(parser.sequence(result, 'type'))
for r in parser.find(result, 'type', 'https'):
    print(r)
find = parser.find(result, 'type', 'https')
print(find)