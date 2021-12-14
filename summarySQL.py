import psycopg2
import sys
import os
import pandas as pd

try:
    conn = psycopg2.connect("dbname='postgres' user='postgres' host='localhost' password='pass1234'")
    print('Success connecting to the database')
except:
    print('I am unable to connect to the database')
    sys.exit()

cursor = conn.cursor()

try:
    cursor.execute("""
    CREATE TABLE SUMMARY (
        summary_id SERIAL PRIMARY KEY,
        "date" VARCHAR(10) NOT NULL,
        "papers" VARCHAR(100) NOT NULL,
        num_articles INTEGER)
    """)
    conn.commit()
except Exception as e:
    cursor.execute("ROLLBACK")
    print('ERROR: ', e)

summary_files = os.listdir('summary/')

for file in summary_files:
    with open('summary/' +  file) as f:
        cursor.copy_from(f, 'summary', columns=('date', 'papers', 'num_articles'), sep=',')


cursor.execute("""SELECT * FROM summary""")
rows = cursor.fetchall()
print(rows[0:4])

cursor.execute("""SELECT COUNT(*) FROM summary""")
rows = cursor.fetchall()
print(rows)