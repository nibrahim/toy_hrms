import argparse
import csv
import logging
import sys

import psycopg2
import sqlalchemy as sa

import db


class HRException(Exception): pass

logger = False

def generate_vcard(lname, fname, designation, email, phone):
    return f"""BEGIN:VCARD
VERSION:2.1
N:{lname};{fname}
FN:{fname} {lname}
ORG:Authors, Inc.
TITLE:{designation}
TEL;WORK;VOICE:{phone}
ADR;WORK:;;100 Flat Grape Dr.;Fresno;CA;95555;United States of America
EMAIL;PREF;INTERNET:{email}
REV:20150922T195243Z
END:VCARD"""


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

    query_parser = subparsers.add_parser("query", help="Get information for a single employee")
    query_parser.add_argument("--vcard", action="store_true", default=False, help="Generate vcard for employee")
    query_parser.add_argument("id", help="employee id")

    args = parser.parse_args()
    return args


def handle_initdb(args):
    db_uri = f"postgresql:///{args.dbname}"
    db.create_all(db_uri)
    session = db.get_session(db_uri)
    d1 = db.Designation(title="CEO", max_leaves=20)
    d2 = db.Designation(title="Engineer", max_leaves=10)
    session.add(d1)
    session.add(d2)
    session.commit()

def handle_import(args):
    db_uri = f"postgresql:///{args.dbname}"
    session = db.get_session(db_uri)

    with open(args.employees_file) as f:
        reader = csv.reader(f)
        for lname, fname, title, email, phone in reader:
            
            q = sa.select(db.Designation).where(db.Designation.title==title)
            designation = session.execute(q).scalar_one()
            
            logger.debug("Inserting %s", email)
            employee = db.Employee(lname=lname,
                                   fname=fname,
                                   title=designation,
                                   email=email,
                                   phone=phone)
            session.add(employee)
        session.commit()
    
def handle_query(args):
    con = psycopg2.connect(dbname=args.dbname)
    cur = con.cursor()
    query = "SELECT fname, lname, designation, email, phone from employees where id = %s"
    cur.execute(query, (args.id,))
    fname, lname, designation, email, phone = cur.fetchone()

    print (f"""Name        : {fname} {lname}
Designation : {designation}
Email       : {email}
Phone       : {phone}""")
    if (args.vcard):
        vcard = generate_vcard(lname, fname, designation, email, phone)
        print (f"\n{vcard}")


    con.close()
            


    


def main():
    try:
        args = parse_args()
        init_logger(args.v)
        ops = {"initdb" : handle_initdb,
               "import" : handle_import,
               "query" : handle_query}
        ops[args.op](args)
    except HRException as e:
        logger.error("Program aborted, %s", e)
        sys.exit(-1)
    

if __name__ == "__main__":
    main()
