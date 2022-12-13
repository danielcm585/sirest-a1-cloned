from sirest.utils import execute_sql

class Food: 
    def __init__(this, tup):
        this.rname = tup[0]
        this.rbranch = tup[1]
        this.foodname = tup[2]
        this.description = tup[3]
        this.stock = tup[4]
        this.price = tup[5]
        this.fcategory = tup[6]

    def json(this):
        category = execute_sql(f"select name from food_category where id = '{this.fcategory}';")[0][0]

        return {
            'rname': this.rname,
            'rbranch': this.rbranch,
            'foodname': this.foodname,
            'description': this.description,
            'stock': this.stock,
            'price': this.price,
            'category': category,
        }