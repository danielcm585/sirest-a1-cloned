class CourierOngoingOrder:
    def __init__(this, tup):
        this.resto = tup[0]
        this.pelanggan = tup[1]
        this.waktuorder = tup[2]
        this.status = tup[3]
        this.emailcust = tup[4]

    def json(this):
        return {
            'resto' : this.resto,
            'pelanggan' : this.pelanggan,
            'waktuorder' : this.waktuorder,
            'status' : this.status,
            'emailcust' : this.emailcust
        }

class DetailPesanan:
    waktuorder = None
    daftarpesanan = None
    namapemesan = None

    def __init__(this, tup):
        this.streetCust = tup[0]
        this.districtCust = tup[1]
        this.cityCust = tup[2]
        this.provinceCust = tup[3]
        this.restoName = tup[4]
        this.streetResto = tup[5]
        this.districtResto = tup[6]
        this.cityResto = tup[7]
        this.provinceResto = tup[8]
        this.totalFood = tup[9]
        this.totalDiscount = tup[10]
        this.totalDelivery = tup[11]
        this.totalPrice = tup[12]
        this.paymentMethod = tup[13]
        this.courierName = tup[14]
        this.courierPlate = tup[15]
        this.courierVType = tup[16]
        this.courierVBrand = tup[17]

    def setWaktuOrder(waktuOrder):
        waktuorder = waktuOrder

    def json(this):
        return{
            'waktuOrder' : this.waktuorder,
            'namaCust' : this.namapemesan,
            'streetCust' :this.streetCust,
            'districtCust' : this.districtCust,
            'cityCust' : this.cityCust,
            'provinceCust' : this.provinceCust,
            'restoName' : this.restoName,
            'streetResto': this.streetResto,
            'districtResto' : this.districtResto,
            'cityResto' : this.cityResto,
            'provinceResto' : this.provinceResto,
            'daftarPesanan' : this.daftarpesanan,
            'totalFood' : this.totalFood,
            'totalDiscount' : this.totalDiscount,
            'totalDelivery' : this.totalDelivery,
            'totalPrice' : this.totalPrice,
            'paymentMethod' : this.paymentMethod,
            'courierName' : this.courierName,
            'courierPlate' : this.courierPlate,
            'courierVType' : this.courierVType,
            'courierVBrand' : this.courierVBrand
        }

class CustomerOngoingOrder:
    def __init__(this, tup):
        this.nama = tup[0]
    
    def json(this):
        return {
            'namacust' : this.nama
        }

class PesananMakanan:
    def __init__(this, tup):
        this.foodname = tup[0]
        this.amount = tup[1]

    # def json(this):
    #     rname = this.rname.replace("'","''")
    #     rbranch = this.rbranch.replace("'","''")
    #     foodname = this.foodname.replace("'","''")
    #     price = execute_sql(f"select price from food where rname = '{rname}' and rbranch = '{rbranch}' and foodname = '{foodname}';")[0][0]
    #     return {
    #         'email': this.email,
    #         'datetime': this.datetime,
    #         'rname': this.rname,
    #         'rbranch': this.rbranch,
    #         'foodname': this.foodname,
    #         'amount': this.amount,
    #         'note': this.note,
    #         'price': price
    #     }

    def json(this):
        return{
            'foodname' : this.foodname,
            'amount' : this.amount
        }