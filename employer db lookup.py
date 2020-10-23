import sqlite3
conn = sqlite3.connect("employer_names.db")
c = conn.cursor()

c.execute("SELECT distinct RAW_NAME, clean_name from employer_pairs where CLEAN_NAME like '%Broad%' order by CLEAN_NAME")
c.fetchall()

