import argparse
import logging
import sys

import psycopg2
# # free line
# import our own (alphabetical order)

class HRException(Exception): pass

logger = False

"""
BEGIN:VCARD
VERSION:2.1
N:{lname};{fname}
FN:{fname} {lname}
ORG:Authors, Inc.
TITLE:{title}
TEL;WORK;VOICE:{phone}
ADR;WORK:;;100 Flat Grape Dr.;Fresno;CA;95555;United States of America
EMAIL;PREF;INTERNET:{email}
REV:20150922T195243Z
END:VCARD
"""

def parse_args():
    parser = argparse.ArgumentParser(description="HR tool")
    parser.add_argument("--dbname", help="Name of database to use", default="hr")
    parser.add_argument("-v", help="Enable verbose debug logging", default=False)
    subparsers = parser.add_subparsers(dest="op")
    subparsers.add_parser("initdb", help="initialise the database")

    args = parser.parse_args()
    return args

def handle_initdb(args):
    with open("data/init.sql") as f:
        sql = f.read()
        print (sql)
    try:
        con = psycopg2.connect(dbname=args.dbname)
    except psycopg2.OperationalError as e:
        raise HRException(f"Database '{args.dbname}' doesn't exist")

def init_logger(is_verbose):
    global logger
    if is_verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logger = logging.getLogger("HR")
    handler = logging.StreamHandler()
    handler.setLevel(level)
    handler.setFormatter(logging.Formatter("[%(levelname)s] | %(filename)s:%(lineno)d | %(message)s"))
    logger.setLevel(logging.DEBUG)
    logger.addHandler(handler)



def main():
    try:
        args = parse_args()
        init_logger(args.v)
        ops = {"initdb" : handle_initdb}
        ops[args.op](args)
    except HRException as e:
        logger.error("Program aborted, %s", e)
        sys.exit(-1)
    

if __name__ == "__main__":
    main()
