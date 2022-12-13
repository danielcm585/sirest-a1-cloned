class TransactionActorAdmin:
    def __init__(this, tup):
        this.email = tup[0]
        this.nama = tup[1]
        this.role = tup[2]

    def json(this):
        return {
            'email' : this.email,
            'nama' : this.nama,
            'role' : this.role,
        }