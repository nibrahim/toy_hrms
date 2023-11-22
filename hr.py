import argparse
import csv
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

def parse_args():
    parser = argparse.ArgumentParser(description="HR tool")
    parser.add_argument("--dbname", help="Name of database to use", default="hr")
    parser.add_argument("-v", help="Enable verbose debug logging", action="store_true", default=False)
    subparsers = parser.add_subparsers(dest="op")
    subparsers.add_parser("initdb", help="initialise the database")

    import_parser = subparsers.add_parser("import", help="Import data from csv file")
    import_parser.add_argument("employees_file", help="List of employees to import")

    args = parser.parse_args()
    return args

def handle_initdb(args):
    with open("data/init.sql") as f:
        sql = f.read()
        logger.debug(sql)
    try:
        con = psycopg2.connect(dbname=args.dbname)
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
    except psycopg2.OperationalError as e:
        raise HRException(f"Database '{args.dbname}' doesn't exist")

def handle_import(args):
    con = psycopg2.connect(dbname=args.dbname)
    cur = con.cursor()
    with open(args.employees_file) as f:
        reader = csv.reader(f)
        for lname, fname, designation, email, phone in reader:
            logger.debug("Inserting %s", email)
            query = "insert into employees(lname, fname, designation, email, phone) values (%s, %s, %s, %s, %s)"
            cur.execute(query, (lname, fname, designation, email, phone))
        con.commit()
    



def main():
    try:
        args = parse_args()
        init_logger(args.v)
        ops = {"initdb" : handle_initdb,
               "import" : handle_import}
        ops[args.op](args)
    except HRException as e:
        logger.error("Program aborted, %s", e)
        sys.exit(-1)
    

if __name__ == "__main__":
    main()
