from sirest.models.user_model import User
from sirest.models.transaction_actor_model import TransactionActor
from sirest.utils import execute_sql

class Restaurant:
    def __init__(this, tup):
        this.rname = tup[0]
        this.rbranch = tup[1]
        this.email = tup[2]
        this.rphonenum = tup[3]
        this.street = tup[4]
        this.district = tup[5]
        this.city = tup[6]
        this.province = tup[7]
        this.rating = tup[8]
        this.rcategory = tup[9]

    def json(this):
        category = execute_sql(f"select name from restaurant_category where id = '{this.rcategory}';")[0][0]
        user = User(execute_sql(f"select * from user_acc where email = '{this.email}';")[0]).json()
        transaction_actor = TransactionActor(execute_sql(f"select * from transaction_actor where email = '{this.email}';")[0]).json()        
        owner_fname = execute_sql(f"select u.fname from restaurant as r inner join user_acc as u on u.email = r.email")
        owner_lname = execute_sql(f"select u.lname from restaurant as r inner join user_acc as u on u.email = r.email")

        return {
            'rname': this.rname,
            'rbranch': this.rbranch,
            'email': this.email,
            'rphonenum': this.rphonenum,
            'street': this.street,
            'district': this.district,
            'city': this.city,
            'province': this.province,
            'rating': this.rating,
            'category': category,
            'user': user,
            'transactionactor': transaction_actor,
            'fname' : owner_fname,
            'lname' : owner_lname
        }

# user -> transaction_actor -> restaurant