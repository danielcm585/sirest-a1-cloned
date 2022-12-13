class BahanMakanan:
    def __init__(this, tup):
        this.id = tup[0]
        this.name = tup[1]

    def json(this):
        return {
            'id': this.id,
            'name': this.name,
        }