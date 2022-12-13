from sirest.utils import execute_sql

class Jam_op: 
    def __init__(this, tup):
        this.day = tup[2]
        this.starthours = tup[3]
        this.endhours = tup[4]


    def json(this):

        return {
            'day': this.day,
            'starthours': this.starthours,
            'endhours': this.endhours,
        }
