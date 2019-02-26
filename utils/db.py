#!/usr/bin/env python3
# coding: utf-8

import sqlite3



def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()


con = sqlite3.connect("pturf.db")

with open('pturf.sql','r') as f :
    txt = f.read()

cursor = con.cursor()
cursor.ex
