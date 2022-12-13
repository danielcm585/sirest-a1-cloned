from sirest.utils import execute_sql

class TransactionHistory:
    def __init__(this, tup):
        this.email = tup[0]
        this.datetime = tup[1]
        this.tsid = tup[2]
        this.datetimestatus = tup[3]

    def json(this):
        status = execute_sql(f"select name from transaction_status where id = '{this.tsid}';")[0][0]
        return {
            'statusid': this.tsid,
            'status': status,
            'timestamp': this.datetimestatus
        }