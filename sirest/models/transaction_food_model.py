from sirest.models.courier_model import Courier
from sirest.utils import execute_sql

class TransactionFood:
    def __init__(this, tup):
        this.email = tup[0]
        this.datetime = tup[1]
        this.rname = tup[2]
        this.rbranch = tup[3]
        this.foodname = tup[4]
        this.amount = tup[5]
        this.note = tup[6]

    def json(this):
        rname = this.rname.replace("'","''")
        rbranch = this.rbranch.replace("'","''")
        foodname = this.foodname.replace("'","''")
        price = execute_sql(f"select price from food where rname = '{rname}' and rbranch = '{rbranch}' and foodname = '{foodname}';")[0][0]
        return {
            'email': this.email,
            'datetime': this.datetime,
            'rname': this.rname,
            'rbranch': this.rbranch,
            'foodname': this.foodname,
            'amount': this.amount,
            'note': this.note,
            'price': price
        }

    # where rname = 'The King\'s Empress'