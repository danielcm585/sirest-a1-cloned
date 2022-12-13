from sirest.models.user_model import User
from sirest.utils import execute_sql

class Courier:
    def __init__(this, tup):
        this.email = tup[0]
        this.platenum = tup[1]
        this.drivinglicensenum = tup[2]
        this.vehicletype = tup[3]
        this.vehiclebrand = tup[4]

    def json(this):
        user = User(execute_sql(f"select * from user_acc where email = '{this.email}';")[0]).json()
        return {
            'email': this.email,
            'platenum': this.platenum,
            'drivinglicensenum': this.drivinglicensenum,
            'vehicletype': this.vehicletype,
            'vehiclebrand': this.vehiclebrand,
            'user': user,
        }