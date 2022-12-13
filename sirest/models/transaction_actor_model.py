from sirest.models.user_model import User
from sirest.utils import execute_sql

class TransactionActor:
    def __init__(this, tup):
        this.email = tup[0]
        this.nik = tup[1]
        this.bankname = tup[2]
        this.accountno = tup[3]
        this.restopay = tup[4]
        this.adminid = tup[5]
        

    def json(this):
        rows_customer = execute_sql(f'''
            SELECT email from customer
            WHERE email = '{this.email}';
        ''')

        rows_restoran = execute_sql(f'''
            SELECT email from restaurant
            WHERE email = '{this.email}';
        ''')

        rows_courier = execute_sql(f'''
            SELECT email from courier
            WHERE email = '{this.email}';
        ''')

        role = ""

        if(len(rows_customer) > 0):
            role = "Pelanggan"
        elif(len(rows_courier) > 0):
            role = "Kurir"
        elif(len(rows_restoran) > 0):
            role = "Restoran"
        else:
            role = "gatau"

        nama = execute_sql(f'''
            SELECT fname , lname from user_acc
            where email = '{this.email}'
        ''')[0]



    
        return {
            'email': this.email,
            'nik': this.nik,
            'bankname': this.bankname,
            'accountno': this.accountno,
            'restopay': this.restopay,
            'adminid': this.adminid,
            'role' : role,
            'nama' : nama[0] + " " + nama[1]
        }