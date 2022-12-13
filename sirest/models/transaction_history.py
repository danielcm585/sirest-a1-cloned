class TransactionHistory:
    def __init__(this, tup):
        this.restaurant_name = tup[0] + " " + tup[1]
        this.customer_name = tup[2] + " " + tup[3]
        this.datetime = tup[4]
        this.transaction_status = tup[5]
    
    def json(this):
        return {
            'restaurant_name': this.restaurant_name,
            'customer_name' : this.customer_name,
            'datetime' : this.datetime,
            'transaction_status' : this.transaction_status
        }
    