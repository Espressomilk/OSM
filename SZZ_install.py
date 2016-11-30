import os
import sys
import getopt

from TableCreation.create_database import *
from TableCreation.create_tables import *

def usage():
    print("usage: SZZ_install.py [-h] [-c host] [-u user] [-p passwd] [-n dbname] [-i input]")
    print("-c:  host connect, for instance 'localhost'")
    print("-u:  username for mysql, for instance 'root'")
    print("-p:  password for mysql, ignore this if no password")
    print("-n:  name for the new database")
    print("-i:  inputfile path, for instance '../shanghai_dump.osm'")


if __name__ == "__main__":
    opts, args = getopt.getopt(sys.argv[1:], "hc:u:p:n:i:", ["help", "host=", "user=", "passwd=", "dbname=", "input="])
    host = ""
    user = ""
    passwd = ""
    dbname = ""
    inputdata = ""
    for op, value in opts:
        if(op == "-c"):
            host = value
        elif(op == "-u"):
            user = value
        elif(op == "-p"):
            passwd = value
        elif(op == "-n"):
            dbname = value
        elif(op == "-i"):
            inputdata = value
        elif(op == "-h"):
            usage()
            sys.exit()

    # print(host, user, passwd, dbname, inputdata)
    print("Create database " + dbname)
    create_database(host, user, passwd, dbname)
    print("Create tables in " + dbname)
    create_tables(host, user, passwd, dbname)
    print("Start insertion...")
    if(passwd == ""):
        os.system('python ./DataInsertion/dumpin.py -c %s -u %s -n %s -i %s' % (host, user, dbname, inputdata))
    else:
        os.system('python ./DataInsertion/dumpin.py -c %s -u %s -p %s -n %s -i %s' % (host, user, passwd, dbname, inputdata))
