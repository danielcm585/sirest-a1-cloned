from sirest.models.courier_model import Courier
from sirest.models.user_model import User
from sirest.models.restaurant_model import Restaurant
from sirest.models.transaction_food_model import TransactionFood
from sirest.models.transaction_history_model import TransactionHistory
from sirest.utils import execute_sql

class Transaction:
    def __init__(this, tup):
        this.email = tup[0]
        this.datetime = tup[1]
        this.street = tup[2]
        this.district = tup[3]
        this.city = tup[4]
        this.province = tup[5]
        this.totalfood = tup[6]
        this.totaldiscount = tup[7]
        this.deliveryfee = tup[8]
        this.totalprice = tup[9]
        this.rating = tup[10]
        this.pmid = tup[11]
        this.psid = tup[12]
        this.dfid = tup[13]
        this.courierid = tup[14]

    def json(this):
        user = User(execute_sql(f"select * from user_acc where email = '{this.email}';")[0]).json()
        rows = execute_sql(f"""
            select * from restaurant where rname in (
                select rname from transaction_food 
                where email = '{this.email}' and datetime = '{this.datetime}'
            ) and rbranch in (
                select rbranch from transaction_food 
                where email = '{this.email}' and datetime = '{this.datetime}'
            );
        """)
        restaurant = None
        if (rows != None and len(rows) > 0): restaurant = Restaurant(rows[0]).json()
        paymentmethod = execute_sql(f"select name from payment_method where id = '{this.pmid}';")[0][0]
        paymentstatus = execute_sql(f"select name from payment_status where id = '{this.psid}';")[0][0]
        rows = execute_sql(f"select * from transaction_history where email = '{this.email}' and datetime = '{this.datetime}';")
        transactionstatus = [ TransactionHistory(row).json() for row in rows ]
        courier = Courier(execute_sql(f"select * from courier where email = '{this.courierid}';")[0]).json()
        courier_name = execute_sql(f"select u.fname, u.lname from user_acc as u where u.email = '{courier['email']}';")
        menus = [ TransactionFood(row).json() for row in execute_sql(f"""
            select * from transaction_food where email = '{this.email}' and datetime = '{this.datetime}';
        """) ]
        
        return {
            'user': user,
            'restaurant': restaurant,
            'email': this.email,
            'datetime': this.datetime,
            'street': this.street,
            'district': this.district,
            'city': this.city,
            'province': this.province,
            'totalfood': this.totalfood,
            'totaldiscount': this.totaldiscount,
            'deliveryfee': this.deliveryfee,
            'totalprice': this.totalprice,
            'rating': this.rating,
            'paymentmethod': paymentmethod,
            'paymentstatus': paymentstatus,
            'transactionstatus': transactionstatus,
            'dfid': this.dfid,
            'courier': courier,
            'menus': menus,
            'couriername': courier_name
        }