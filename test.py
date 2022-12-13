import os
import dj_database_url
from dotenv import load_dotenv
from sirest.utils import *

load_dotenv()



cursor = connection.cursor()
cursor.execute('set search_path = sirest_a1;')

cursor.execute(sql)

rows = None
try: rows = cursor.fetchall()
except: print('No output')

connection.commit()
cursor.close()

return rows

items = execute_sql("""
    select * 
    from test 
    where test_col = 'dunia UwU';
""")
print(items)
print(len(items))