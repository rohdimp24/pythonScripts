'''this is a test file to connect to a postgres database and perform the CRUD operations'''
import psycopg2
#for some reason the user has to be postgres and not root
conn = psycopg2.connect(database='jim', user='postgres', password='root', host='127.0.0.1', port='5432')
cur = conn.cursor()
cur.execute("""Select * from cases.smartsignal_jim_allfields where "equipmentType"='WIND_TURBINE'""")
rows = cur.fetchall()

#display the rows
for row in rows:
    print (row[0])