import argparse
import json
import os
from lib.EDIParser import EDIParser

def set_args(subparsers):
    parser = subparsers.add_parser('parse', description='parsing of edi to supported formats and generation of messages')
    parser.add_argument('--from', dest='from_type', choices=['edi', 'json'], default='edi'),
    parser.add_argument('--to', dest='to_type', choices=['json', 'raw', 'json-arr', 'edi'], default='json')
    parser.add_argument('--aperak', action='store_true')

def run(args):
    payload = args.input.read()
    parser = EDIParser(payload, format=args.from_type)

    work_result = None
    if args.aperak is True:
        work_result = parser.create_aperak()

    to_type = args.to_type
    if to_type == 'json':
        result = json.dumps(parser.toDict(work_result))
    elif to_type == 'json-arr':
        result = json.dumps(parser.toList(work_result))
    elif to_type == 'edi':
        result = parser.toEdi(work_result)
        result = result.replace("'", "'\n") # pretty print
    elif to_type == 'raw':
        result = payload

    print(result)