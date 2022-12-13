from sirest.models.user_model import User
from sirest.models.transaction_actor_model import TransactionActor
from sirest.utils import execute_sql

class Customer:
    def __init__(this, tup):
        this.email = tup[0]
        this.birthdate = tup[1]
        this.sex = tup[2]

    def json(this):
        user = User(execute_sql(f"select * from user_acc where email = '{this.email}';")[0]).json()
        transaction_actor = TransactionActor(execute_sql(f"select * from transaction_actor where email = '{this.email}';")[0]).json()
        return {
            'email': this.email,
            'birthdate': this.birthdate,
            'sex': this.sex,
            'user': user,
            'transactionactor': transaction_actor,
        }