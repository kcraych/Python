#!/usr/bin/python

import pyodbc
import csv
import re
from codecs import open
from datetime import datetime
import sys, traceback

class ExecuteSQLCode(object):

    def __init__(self, path, prv, svr, db, usr, pwd, rtn):
        conn1 = ExecuteSQLCode.Connect2SQL(prv, svr, db, usr, pwd)
        commands = ExecuteSQLCode.ReadFileScript(path)
        print(ExecuteSQLCode.ExecuteCommands(commands, conn1, rtn))

    def ReadFileScript(filename):
        # Open and read the file as a single buffer
        fd = open(filename, mode='r', encoding='utf-8-sig')
        sqlFile = fd.read()
        fd.close()

        sqlCommands = sqlFile.split("/*PyBreak*/")
        return sqlCommands

    def Connect2SQL(driver, server, db, uid, pwd):
        try:
            cnxn = pyodbc.connect('driver={%s};server=%s;database=%s;uid=%s;pwd=%s;' % (driver, server, db, uid, pwd))
        except:
            current_datetime = str(datetime.now())
            print(current_datetime + " - Unable to connect to database. Error: " + traceback.format_exc())
            sys.exit(1)
        return cnxn

    def ExecuteCommands(commands, connection, returnrows):
        cursor = connection.cursor()
        for command in commands:
            try:
                if returnrows == 1:
                    rows = cursor.execute(command)
                else:
                    cursor.execute(command)
                    connection.commit()
            except:
                current_datetime = str(datetime.now())
                print(current_datetime + " - Unable to execute script. Error: " + traceback.format_exc())
                sys.exit(1)

        result = []
        if returnrows == 1:
            for row in rows:
                result.append(row)
        else:
            "Do Nothing"

        return result