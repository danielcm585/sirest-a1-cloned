from django.db import connection

def execute_sql(sql):
    cursor = connection.cursor()
    cursor.execute('set search_path = sirest_a1;')
    
    cursor.execute(sql)

    rows = None
    try: rows = cursor.fetchall()
    except: print('No output')

    connection.commit()
    cursor.close()

    return rows