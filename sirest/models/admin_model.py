from sirest.models.user_model import User
from sirest.utils import execute_sql

class Admin:
    def __init__(this, tup):
        this.email = tup[0]

    def json(this):
        user = User(execute_sql(f"select * from user_acc where email = '{this.email}';")[0]).json()
        return {
            'email': this.email,
            'user': user,
        }