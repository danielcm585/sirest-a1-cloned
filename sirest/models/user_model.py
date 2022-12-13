class User:
    def __init__(this, tup):
        this.email = tup[0]
        this.password = tup[1]
        this.phonenum = tup[2]
        this.fname = tup[3]
        this.lname = tup[4]

    def json(this):
        return {
            'email': this.email,
            'phonenum': this.phonenum,
            'fname': this.fname,
            'lname': this.lname,
        }