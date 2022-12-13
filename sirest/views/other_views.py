from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view
from sirest.forms import *
from sirest.views.general_views import *
from sirest.models.payment_method_model import PaymentMethod
from sirest.utils import execute_sql
import random
from sirest.models.transaction_model import *
from django.core import serializers
from datetime import datetime


# def riwayat_transaksi_pesanan(request):
#     is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
#     role = request.COOKIES.get('role')
#     if (not is_logged_in): return index(request)
#     # TODO: Check role, otherwise return forbidden(request)
#     context = {
#         'is_logged_in': is_logged_in,
#         'name': request.COOKIES.get('name'),
#         'role': role,
#     }
#     return render(request, 'other/riwayat-pesanan.html')

# def riwayat_transaksi_pesanan(request):
#     context = {
#         'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
#         'name': request.COOKIES.get('name'),
#         'role': request.COOKIES.get('role'),
#     }
#     return render(request, 'other/riwayat-pesanan.html', context)

# @api_view(['GET'])
def riwayat_transaksi_pesanan_api(request):
    def get():
        data = {}
        data['is_logged_in'] = bool(request.COOKIES.get('is_logged_in') == 'True')
        data['role'] = request.COOKIES.get('role')
        data['name'] = request.COOKIES.get('name')
        fname = data['name'].split()[0]
        lname = data['name'].split()[1]
        data['fname'] = fname
        data['lname'] = lname
        # rows = execute_sql("""
        #         SELECT * FROM transaction AS T WHERE 
        #         T.Email in (
        #             SELECT TH.Email FROM transaction_history AS TH WHERE 
        #             T.email = TH.email and T.datetime = TH.datetime and 
        #             TH.tsid in ('0000000000000000000000005', '0000000000000000000000004')
        #         ) AND T.Datetime in (
        #             SELECT TH.Datetime FROM transaction_history AS TH WHERE 
        #             T.email = TH.email and T.datetime = TH.datetime and 
        #             TH.tsid in ('0000000000000000000000005', '0000000000000000000000004')
        #         );      
        # """)


        
        # transactions = [Transaction(row).json() for row in rows]
        
        # for i in range(len(transactions)):
        #     transactions[0]['transactionstatus'].reverse()
        
        # return JsonResponse(transactions, safe=False, status=200)
        
        
        transaction_history_data = []
        if(data['role'] == 'Kurir'):
            rows = execute_sql(f'''
            SELECT TF.RName, TF.RBranch, U.FName, U.LName, T.Datetime, TS.name, T.rating, U.Email FROM TRANSACTION_HISTORY AS TH
            INNER JOIN TRANSACTION AS T 
            ON T.Email = TH.Email AND T.Datetime = TH.Datetime 
            INNER JOIN COURIER AS C
            ON T.courierid = C.email 
            INNER JOIN TRANSACTION_ACTOR AS TA
            ON T.email = TA.email
            INNER JOIN USER_ACC AS U
            ON TA.email = U.email
            INNER JOIN TRANSACTION_FOOD AS TF
            ON T.email = TF.email
            INNER JOIN TRANSACTION_STATUS AS TS
            ON TH.tsid = TS.id
            WHERE C.email = '{request.email}'
            AND TH.tsid in ('0000000000000000000000005', '0000000000000000000000004');
            ''')

            for i in range(len(rows)):
                transaction_history_data.append({
                    "restaurant_name" : rows[i][0] + " " + rows[i][1],
                    "customer_name" : rows[i][2] + " " + rows[i][3],
                    "datetime" : rows[i][4].strftime("%Y-%m-%d %H:%M:%S"),
                    "date":rows[i][4],
                    "transaction_status" : rows[i][5],
                    "rating" : rows[i][6],
                    "rating" : rows[i][7],

            })
        elif(data['role'] == 'Pelanggan'):
            rows = execute_sql(f'''
                SELECT TF.RName, TF.RBranch, U.FName, U.LName,T.Datetime, TS.name, T.email, T.rating FROM TRANSACTION_HISTORY AS TH
                INNER JOIN TRANSACTION AS T 
                ON T.Email = TH.Email AND T.Datetime = TH.Datetime 
                INNER JOIN USER_ACC AS U
                ON T.courierid = U.email
                INNER JOIN TRANSACTION_FOOD AS TF
                ON T.email = TF.email
                INNER JOIN TRANSACTION_STATUS AS TS
                ON TH.tsid = TS.id
                WHERE T.email = '{request.email}'AND 
                TH.tsid in ('0000000000000000000000005', '0000000000000000000000004');
                
            ''')

            for i in range(len(rows)):
                    
                    if(rows[i][7] is None):
                        sudah_dinilai = False
                    else:
                        sudah_dinilai = True

                    transaction_history_data.append({
                        "restaurant_name" : rows[i][0] + " " + rows[i][1],
                        "courier_name" : rows[i][2] + " " + rows[i][3],
                        "date":rows[i][4],
                        "datetime" : rows[i][4].strftime("%Y-%m-%d %H:%M:%S"),
                        "transaction_status" : rows[i][5],
                        "rating" : rows[i][7],
                        "email" : rows[i][6],
                        "sudah_dinilai" : sudah_dinilai

                })
        elif data['role'] == 'Restoran':



            restaurant = execute_sql(f'''
                SELECT * FROM RESTAURANT
                WHERE email = '{request.email}';
            ''')[0]

            rows = execute_sql(f'''
                SELECT t.email, t.datetime, ua.fname,ua.lname, th.tsid from transaction_history as th
                inner join transaction as t
                on th.email = t.email and th.datetime = t.datetime
                inner join transaction_food as tf
                on tf.email = t.email and tf.datetime = t.datetime
                INNER join user_acc as ua
                on ua.email = t.courierid
                WHERE TF.rname = '{restaurant[0].replace("'","''")}'AND TF.rbranch = '{restaurant[1].replace("'","''")}' AND 
                TH.tsid in ('0000000000000000000000005', '0000000000000000000000004');
            ''')

            

            print(rows)

            for i in range (len(rows)):
                status = execute_sql(f'''
                SELECT name from transaction_status 
                where id = '{rows[i][4]}';
                ''')[0]
                pembeli = execute_sql(f'''
                    SELECT fname, lname from user_acc
                    where email = '{rows[i][0]}';
                ''')[0]
                transaction_history_data.append({
                    "email" : rows[i][0],
                    "nama_pembeli" : pembeli[0] + " " + pembeli[1],
                    "datetime" : rows[i][1].strftime("%Y-%m-%d %H:%M:%S"),
                    "courier_name" : rows[i][2] + " " + rows[i][3],
                    "status" : status[0]
                    
                })





            
        
        data['transaction_history'] = transaction_history_data
        # lasttransactionstatus = transactions['transactionstatus'][len(transactions['transactionstatus'])-1]['status']
        # data['lasttransactionstatus'] = lasttransactionstatus
        return render(request, 'other/riwayat-pesanan.html', {'data' : data})
    if (request.method == 'GET'): return get()

def riwayat_detail(request, email, datetime):
    data = {}
    data['is_logged_in'] = bool(request.COOKIES.get('is_logged_in') == 'True')
    data['role'] = request.COOKIES.get('role')
    data['name'] = request.COOKIES.get('name')

    if(request.COOKIES.get('role') == 'Pelanggan'):
        pemesan = request.COOKIES.get('name')
        print(pemesan)
    else:
        nama = execute_sql(f'''
            SELECT fname, lname from user_acc
            WHERE email = '{email}';
        ''')[0]
        pemesan = nama[0] + " " +  nama[1]

    transaksi_stuff = execute_sql(f'''
        SELECT * FROM TRANSACTION_HISTORY AS TH
        INNER JOIN TRANSACTION AS T
        ON TH.email = T.email and TH.datetime = T.datetime
        WHERE TH.email = '{email}' and TH.datetime = '{datetime}';
    ''')[0]

    transaction_courier = execute_sql(f'''
        SELECT * FROM USER_ACC AS UA 
        INNER JOIN COURIER AS C
        ON C.email = UA.email
        WHERE C.email = '{transaksi_stuff[18]}';
    ''')[0]

    transaction_food = execute_sql(f'''
        SELECT TF.rname, TF.rbranch, TF.foodname, TF.amount, TF.note
        FROM transaction_food as TF
        where TF.email = '{email}' and TF.datetime = '{datetime}';
    ''')

    transaction_restaurant = execute_sql(f'''
        SELECT * from restaurant as r
        where r.rname = '{transaction_food[0][0].replace("'","''")}' and r.rbranch = '{transaction_food[0][1].replace("'","''")}' ;
    ''')[0]

    # restaurant = {
    #     'rname' : transaction_food[0][0],
    #     'rbranch' : transaction_food[0][1]
    # }

    food_order = []

    for i in range(len(transaction_food)):
        food_order.append({
            'foodname' : transaction_food[i][2],
            'amount' : transaction_food[i][3],
            'notes' : transaction_food[i][4]

        })
    
    payment_status = execute_sql(f'''
        SELECT name FROM payment_status
        WHERE id = '{transaksi_stuff[16]}';
    ''')[0]

    transaction_status = execute_sql(f'''
        SELECT TS.name from transaction_status AS TS
        INNER JOIN TRANSACTION_HISTORY AS TH
        ON TS.id = TH.tsid
        WHERE TH.email = '{email}' and TH.datetime = '{datetime}';
    ''')[0]

    payment_method = execute_sql(f'''
        SELECT name from payment_method
        where id = '{transaksi_stuff[16]}';
    ''')[0]

    status_timestamp = []

    status_time = execute_sql(f'''
        SELECT TS.name , TH.datetimestatus FROM 
        TRANSACTION_HISTORY AS TH
        INNER JOIN TRANSACTION_STATUS AS TS
        ON TS.id = TH.tsid
        WHERE TH.email = '{email}' and TH.datetime = '{datetime}';

    ''')

    for i in range (len(status_time)):
        status_timestamp.append({
            "status" : status_time[i][0],
            "timestamp" : status_time[i][1]
        })

    # print(status_time)
    # print(transaction_courier)
    # print(transaction_food)
    # print(transaction_restaurant)
    print(transaksi_stuff[11])

    data['detail_transaksi']  = [{
        "waktu_pemesanan" : datetime,
        "nama_pemesan" : pemesan,
        "jalan_pemesan" : transaksi_stuff[6],
        "kecamatan_pemesan" : transaksi_stuff[7],
        "kota_pemesan" : transaksi_stuff[8],
        "provinsi_pemesan" : transaksi_stuff[9],
        "nama_cabang_restoran" : transaction_food[0][0] + " " + transaction_food[0][1],
        "jalan_restoran" : transaction_restaurant[4],
        "kecamatan_restoran" : transaction_restaurant[5],
        "kota_restoran" : transaction_restaurant[6],
        "provinsi_restoran" : transaction_restaurant[7],
        "makanan_dipesan" : food_order,
        "total_harga_makanan" : transaksi_stuff[13],
        "total_diskon" : transaksi_stuff[11],
        "biaya_pengantaran" : transaksi_stuff[12],
        "total_biaya" : transaksi_stuff[13] + transaksi_stuff[11] + transaksi_stuff[12],
        "jenis_pembayaran" : payment_method,
        "status_pembayaran" : payment_status[0],
        "status_pesanan" : transaction_status[0],
        "nama_kurir" : transaction_courier[3] + " " + transaction_courier[4],
        "plat" : transaction_courier[6],
        "jenis_kendaraan" : transaction_courier[8],
        "merk_kendaraan" : transaction_courier[9],
        "status_timestamp" : status_timestamp
    }]
    return render(request, 'other/detail-pesanan.html', {"data" : data})


def nilai_pesanan(request, email, datetime):
    data = {}
    data['is_logged_in'] = bool(request.COOKIES.get('is_logged_in') == 'True')
    data['role'] = request.COOKIES.get('role')
    data['name'] = request.COOKIES.get('name')

    if request.method == "POST":
        # body = request.POST.get 
        # rating = body('nilai', False)
        # print(request.POST.get('nilai', False))
        
        # datetime =  datetime.datetime.strptime(datetime, '%d-%m-%Y %H:%M:%S')
        # datetime = datetime.strftime("%Y-%m-%d %H:%M:%S")
        print(f'''
            UPDATE transaction
            SET rating = {request.POST.get('nilai', False)}
            WHERE email = '{email}' and datetime = '{datetime}';
        ''')
        execute_sql(f'''
            UPDATE transaction
            SET rating = {request.POST.get('nilai', False)}
            WHERE email = '{email}' and datetime = '{datetime}';
        ''')
        

        return redirect('/riwayat-transaksi-pesanan/')

        
    
    return render(request, 'other/form-nilai.html', {'data': data})

def food(request):
    
    context = { 
        'is_logged_in': (request.COOKIES.get('is_logged_in') == 'True'),
    }
    return render(request, 'other/food.html', context)
    
@api_view(['GET'])
def payment_method_api(request):
    def get():
        # Get all payment methods
        rows = execute_sql("select * from payment_method;")
        json = [ PaymentMethod(row).json() for row in rows ]
        return JsonResponse(json, safe=False, status=200)

    if (request.method == 'GET'): return get()

def pilih_promo(request):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }


    return render(request, 'other/buat-promo.html', context)

def promo_minimum_transaksi(request):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }

    if request.method == "POST":
        body = request.POST.get 
        namaPromo = body('namaPromo', False)
        diskon = body('diskon', False)
        minimum_trans = body('mintrans', False)
        id = str(execute_sql("select count(*) from promo;")[0][0]+1).rjust(25,'0')
        print(id)

        execute_sql(f'''
            INSERT INTO PROMO values(
                '{id}', '{namaPromo}', '{diskon}'
            );
        ''')

        execute_sql(f'''
            INSERT INTO min_transaction_promo values(
                '{id}', '{minimum_trans}'
            );
        ''')
        return redirect('/daftar-promo/')


    return render(request, 'other/form-pmt.html', context)

def promo_hari_spesial(request):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }

    if request.method == "POST":
        body = request.POST.get 
        namaPromo = body('namaPromo', False)
        diskon = body('diskon', False)
        tanggal = body('tanggal', False)
        id = str(execute_sql("select count(*) from promo;")[0][0]+1).rjust(25,'0')
        print(id)
        execute_sql(f'''
            INSERT INTO PROMO values(
                '{id}', '{namaPromo}', '{diskon}'
            );
        ''')
       
        execute_sql(f'''
            INSERT INTO special_day_promo values(
                '{id}', '{tanggal}'
            );
        ''')
        return redirect('/daftar-promo/')


    return render(request, 'other/form-phs.html', context)

def promo(request):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }
    return render(request, 'other/crud-promo.html', context)

def daftar_promo(request):
    data = {}
    data['is_logged_in'] = bool(request.COOKIES.get('is_logged_in') == 'True')
    data['role'] = request.COOKIES.get('role')
    data['name'] = request.COOKIES.get('name')
    daftar_promo = []
    # rows_special = execute_sql(f'''
    #     SELECT P.Id, P.PromoName, P.Discount, SP.Date FROM PROMO AS P
    #     INNER JOIN SPECIAL_DAY_PROMO AS SP
    #     ON P.Id = SP.Id;
    # ''')
    # rows_min_transaction = execute_sql(f'''
    #     SELECT P.Id, P.PromoName, P.Discount, MT.MinimumTransactionNum FROM PROMO AS P
    #     INNER JOIN MIN_TRANSACTION_PROMO AS MT
    #     ON MT.Id = P.Id;
    # ''')

    rows_promo = execute_sql(f'''
        SELECT P.Id , P.promoname from promo as p;
    ''')

    special_id = execute_sql(f'''
        SELECT id from special_day_promo;
    ''')

    rows_cannot_delete = execute_sql(f'''
        SELECT pid FROM restaurant_promo;
    ''')
    print(rows_cannot_delete)



    cannot_delete = []
    special_id_list = []
    for i in range(len(rows_cannot_delete)):
        cannot_delete.append(rows_cannot_delete[i][0])

    for i in range(len(special_id)):
        special_id_list.append(special_id[i][0])
    print(special_id_list)
    for i in range(len(rows_promo)):
        if rows_promo[i][0] in cannot_delete:
            if rows_promo[i][0] in special_id_list:
                daftar_promo.append(
                    {
                        "pk" : rows_promo[i][0],
                        "nama_promo" : rows_promo[i][1],
                        "jenis_promo" : "Promo Hari Spesial",
                        "delete" : 'false'
                    }
                )
            else :
                daftar_promo.append(
                    {
                        "pk" : rows_promo[i][0],
                        "nama_promo" : rows_promo[i][1],
                        "jenis_promo" : "Promo Minimum Transaksi",
                        "delete" : 'false'
                    }
                )
        else:
            if rows_promo[i][0] in special_id_list:
                daftar_promo.append(
                    {
                       "pk" : rows_promo[i][0],
                        "nama_promo" : rows_promo[i][1],
                        "jenis_promo" : "Promo Hari Spesial",
                        "delete" : 'true'
                    }
                )
            else :
                daftar_promo.append(
                    {
                        "pk" : rows_promo[i][0],
                        "nama_promo" : rows_promo[i][1],
                        "jenis_promo" : "Promo Minimum Transaksi",
                        "delete" : 'true'
                    }
                )

    data["daftar_promo"] = daftar_promo

    return render(request, 'other/daftar-promo.html', {"data" : data})

def daftar_promo_restaurant(request):
    data = {}
    data['is_logged_in'] = bool(request.COOKIES.get('is_logged_in') == 'True')
    data['role'] = request.COOKIES.get('role')
    data['name'] = request.COOKIES.get('name')
    restaurant = execute_sql(f'''
        SELECT rname, rbranch from restaurant
        WHERE email = '{request.email}'
    ''')[0]

    daftar_promo = []

 
    rows = execute_sql(f'''
        SELECT p.promoname, p.discount, rp.start_promo, rp.end_promo, p.id FROM restaurant_promo AS RP
        INNER JOIN promo as p 
        ON RP.pid = p.id
        WHERE RP.rname = '{restaurant[0].replace("'","''")}' and RP.rbranch = '{restaurant[1]}';
    ''')

    rows_hs = execute_sql(f'''
        SELECT id FROM special_day_promo;
    ''')
   
    promo_hari_spesial = []
    
    for i in range(len(rows_hs)):
        promo_hari_spesial.append(rows_hs[i][0])

   

    for i in range(len(rows)):
        if rows[i][4] in promo_hari_spesial:
            daftar_promo.append({
                "pk" : rows[i][4],
                "name" : rows[i][0],
                "discount" : rows[i][1],
                "start_promo" : rows[i][2],
                "end_promo" : rows[i][3],
                "jenis_promo" : "Promo Hari Spesial"
            })
        else:
            daftar_promo.append({
                "pk" : rows[i][4],
                "name" : rows[i][0],
                "discount" : rows[i][1],
                "start_promo" : rows[i][2],
                "end_promo" : rows[i][3],
                "jenis_promo" : "Promo Minimum Transaksi"
            })
    data['daftar_promo'] = daftar_promo
    return render(request,'other/daftar-promo-restoran.html', {'data' : data})

    

def detail_promo_hs(request, pk):
    data = {}
    data['is_logged_in'] = bool(request.COOKIES.get('is_logged_in') == 'True')
    data['role'] = request.COOKIES.get('role')
    data['name'] = request.COOKIES.get('name')
    rows = execute_sql(f'''
    SELECT P.Id, P.PromoName, P.Discount, SP.Date FROM PROMO AS P
    INNER JOIN SPECIAL_DAY_PROMO AS SP
    ON P.Id = SP.Id
    WHERE P.Id = '{pk}'; 
    ''')[0]
        
    
    detail_promo={
        "Id" : rows[0],
        "nama" : rows[1],
        "discount": rows[2],
        "spesial" : rows[3]
    }
    data['detail_promo'] = detail_promo
    print(data)
    return render(request, 'other/detail-promo-hs.html', {'data' : data})

def detail_promo_min(request, pk):
    data = {}
    data['is_logged_in'] = bool(request.COOKIES.get('is_logged_in') == 'True')
    data['role'] = request.COOKIES.get('role')
    data['name'] = request.COOKIES.get('name')

    rows = execute_sql(f'''
        SELECT P.Id, P.PromoName, P.Discount, MT.MinimumTransactionNum FROM PROMO AS P
        INNER JOIN MIN_TRANSACTION_PROMO AS MT
        ON MT.Id = P.Id
        WHERE P.Id = '{pk}';
        ''')[0]
    detail_promo= {
        "Id" : rows[0],
        "nama" : rows[1],
        "discount": rows[2],
        "min" : rows[3]
    }
    data['detail_promo'] = detail_promo
    return render(request, 'other/detail-promo-min.html', {'data' : data})

def detail_promo_resto(request, pk):
    data = {}
    data['is_logged_in'] = bool(request.COOKIES.get('is_logged_in') == 'True')
    data['role'] = request.COOKIES.get('role')
    data['name'] = request.COOKIES.get('name')

    rows = execute_sql(f'''
        SELECT P.id , P.promoname, P.discount, RP.start_promo, RP.end_promo
        FROM PROMO AS P
        INNER JOIN restaurant_promo as RP
        ON RP.pid = P.id
        WHERE p.id = '{pk}';
    ''')[0]

    rows_hs = execute_sql(f'''
        SELECT id FROM special_day_promo;
    ''')
   
    promo_hari_spesial = []
    
    for i in range(len(rows_hs)):
        promo_hari_spesial.append(rows_hs[i][0])
    
    if rows[0] in promo_hari_spesial:
        detail_promo= {
        "Id" : rows[0],
        "nama" : rows[1],
        "discount": rows[2],
        "start_promo" : rows[3],
        "end_promo" : rows[4],
        "jenis" : "Promo Hari Spesial"
        }
    else:
        detail_promo= {
        "Id" : rows[0],
        "nama" : rows[1],
        "discount": rows[2],
        "start_promo" : rows[3],
        "end_promo" : rows[4],
        "jenis" : "Promo Minimum Transaksi"
        }

    data['detail_promo'] = detail_promo
    return render(request, 'other/detail-promo-resto.html', {'data' : data})

def ubah_promo_resto(request, pk):
    data = {}
    data['is_logged_in'] = bool(request.COOKIES.get('is_logged_in') == 'True')
    data['role'] = request.COOKIES.get('role')
    data['name'] = request.COOKIES.get('name')

    rows = execute_sql(f'''
        SELECT P.Id, P.PromoName, P.Discount FROM PROMO AS P
        INNER JOIN RESTAURANT_PROMO AS RP
        ON RP.pid = P.Id
        WHERE P.Id = '{pk}';
        ''')[0]

    rows_hs = execute_sql(f'''
        SELECT id FROM special_day_promo;
    ''')
    
    promo_hari_spesial = []
    
    for i in range(len(rows_hs)):
        promo_hari_spesial.append(rows_hs[i][0])
    
    if rows[0] in promo_hari_spesial:
        promo_diubah = {
        "pk" : rows[0],
        "jenis" : "Promo Hari Spesial",
        "nama" : rows[1],
        "diskon" : rows[2]
        }
    else:
        promo_diubah = {
        "pk" : rows[0],
        "jenis" : "Promo Minimum Transaksi",
        "diskon" : rows[2],
        "nama" : rows[1]
        }

    data['promo_diubah'] = promo_diubah
    if request.method != "POST":
        return render(request, 'other/form-ubah-promo-resto.html', {'data' : data})
    
    body = request.POST
    tanggal_mulai = body['start_time']
    tanggal_berakhir = body['end_time']

    execute_sql(f'''
        UPDATE restaurant_promo
        SET start_promo = '{tanggal_mulai}', 
        end_promo = '{tanggal_berakhir}'
        WHERE pid = '{pk}';
    ''')

    return redirect('/daftar-promo-resto')

def hapus_promo_resto(request, pk):
    data = {}
    data['is_logged_in'] = bool(request.COOKIES.get('is_logged_in') == 'True')
    data['role'] = request.COOKIES.get('role')
    data['name'] = request.COOKIES.get('name')

    execute_sql(f'''
        DELETE FROM RESTAURANT_PROMO
        WHERE pid = '{pk}';
    ''')

    return redirect('/daftar-promo-resto')

    




def ubah_promo_min(request, pk):
    data = {}
    data['is_logged_in'] = bool(request.COOKIES.get('is_logged_in') == 'True')
    data['role'] = request.COOKIES.get('role')
    data['name'] = request.COOKIES.get('name')

    rows = execute_sql(f'''
        SELECT P.Id, P.PromoName, P.Discount, MT.MinimumTransactionNum FROM PROMO AS P
        INNER JOIN MIN_TRANSACTION_PROMO AS MT
        ON MT.Id = P.Id
        WHERE P.Id = '{pk}';
        ''')[0]
    
    nama_jenis_promo = {
        "jenis" : "Promo Minimum Transaksi",
        "nama" : rows[1]
    }

    data["nama_jenis_promo"] = nama_jenis_promo

    if request.method != "POST":
        return render(request, 'other/form-ubah-promosi-min.html', {'data' : data})



    body = request.POST.get
    diskon = body('diskon', False)
    minTransaksi = body('minTransaksi', False)

    execute_sql(f'''
        UPDATE MIN_TRANSACTION_PROMO
        SET minimumtransactionnum = {minTransaksi}
        WHERE id = '{pk}';
    ''')

    execute_sql(f'''
        UPDATE PROMO
        SET discount = {diskon}
        WHERE id = '{pk}'
    ''')
    return redirect('/daftar-promo')

def ubah_promo_hs(request, pk):
    data = {}
    data['is_logged_in'] = bool(request.COOKIES.get('is_logged_in') == 'True')
    data['role'] = request.COOKIES.get('role')
    data['name'] = request.COOKIES.get('name')

    rows = execute_sql(f'''
    SELECT P.Id, P.PromoName, P.Discount, SP.Date FROM PROMO AS P
    INNER JOIN SPECIAL_DAY_PROMO AS SP
    ON P.Id = SP.Id
    WHERE P.Id = '{pk}'; 
    ''')[0]
    
    nama_jenis_promo = {
        "jenis" : "Promo Hari Spesial",
        "nama" : rows[1]
    }

    data["nama_jenis_promo"] = nama_jenis_promo

    if request.method != "POST":
        return render(request, 'other/form-ubah-promo-hs.html', {'data' : data})



    body = request.POST.get
    diskon = body('diskon', False)
    datetime = body('datetime', False)
    # tanggal = datetime.split("/")
    # year = tanggal[0:4]
    # month = tanggal[5:7]
    # date = tanggal[8:10]
    # dateinput = f"{year}-{month}-{date}"


    execute_sql(f'''
        UPDATE SPECIAL_DAY_PROMO
        SET date = '{datetime}'
        WHERE id = '{pk}';
    ''')

    execute_sql(f'''
        UPDATE PROMO
        SET discount = {diskon}
        WHERE id = '{pk}'
    ''')
    return redirect('/daftar-promo')

def delete_promo(request, pk):
    execute_sql(f'''
        DELETE FROM PROMO
        WHERE id = '{pk}'
    ''')
    return redirect('/daftar-promo')
    
def tambah_promo_resto(request):
    data = {}
    data['is_logged_in'] = bool(request.COOKIES.get('is_logged_in') == 'True')
    data['role'] = request.COOKIES.get('role')
    data['name'] = request.COOKIES.get('name')
    daftar_promo = []
    rows = execute_sql(f'''
        SELECT P.Id, P.PromoName, P.Discount FROM PROMO as p;
    ''')

    rows_hs = execute_sql(f'''
        SELECT id from special_day_promo;
    ''')

    promo_hari_spesial = []
    
    for i in range(len(rows_hs)):
        promo_hari_spesial.append(rows_hs[i][0])

    for i in range(len(rows)):
        if rows[i][0] in promo_hari_spesial:
            daftar_promo.append({
                "pk": rows[i][0],
                "nama" : rows[i][1],
                "diskon" : rows[i][2],
                "jenis": "Promo Hari Spesial"
            })
        else:
            daftar_promo.append({
                "pk": rows[i][0],
                "nama" : rows[i][1],
                "diskon" : rows[i][2],
                "jenis": "Promo Minimum Transaksi"
            })
    data['daftar_promo'] = daftar_promo
    if request.method != 'POST':
        return render(request, 'other/form-tambah-promo-resto.html', {'data': data})
    
    body = request.POST.get
    start_date = body('startPromo', False)
    end_date = body('endPromo', False)
    promoname = body('namaPromoResto', False)

    restaurant_food = execute_sql(f'''
        SELECT R.rname, R.rbranch, F.foodname from restaurant as R
        INNER JOIN food AS F
        ON F.rname = R.rname and F.rbranch = R.rbranch
        WHERE R.email = '{request.email}'
    ''')[0]

    promo_id = execute_sql(f'''
        SELECT id from promo
        WHERE promoname = '{promoname}';
    ''')[0][0]

    #gimana ambil promo id nya....
    execute_sql(f'''
        INSERT INTO restaurant_promo values(
            '{restaurant_food[0].replace("'","''")}', '{restaurant_food[1].replace("'","''")}', '{restaurant_food[2]}', '{promo_id}', '{start_date}', '{end_date}'
        );
    ''')

    return redirect('/daftar-promo-resto')

def get_promo_detail(request):
    namaPromoResto = request.GET.get('namaPromoResto')
    rows = execute_sql(f'''
        SELECT P.id, P.Discount FROM PROMO as p
        WHERE p.promoname = '{namaPromoResto}';
    ''')[0]

    rows_hs = execute_sql(f'''
        SELECT id from special_day_promo;
    ''')


    promo_hari_spesial = []
    
    for i in range(len(rows_hs)):
        promo_hari_spesial.append(rows_hs[i][0])

    if rows[0] in promo_hari_spesial:
        return JsonResponse({
            "diskon" : rows[1],
            "jenis" : "Promo Hari Spesial"
        })
    else:
        return JsonResponse({
            "diskon" : rows[1],
            "jenis" : "Promo Minimal Transaksi"
        })



def transaksi_pesanan(request):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }

    email = request.COOKIES.get('email')

    command = execute_sql(
        f''' select rname, rbranch from restaurant where email = '{email}' '''
    )[0]

    context['rname'] = command[0]
    context['rbranch'] = command[1]

    print(context['rname'])
    print(context['rbranch'])

    command = execute_sql(
        f''' select fname, lname, transaction_food.datetime, transaction_status.name, user_acc.email from transaction_food, transaction_history, transaction_status, user_acc where transaction_food.email = transaction_history.email and transaction_food.datetime = transaction_history.datetime and transaction_history.tsid = transaction_status.id and rname = '{context['rname']}' and rbranch = '{context['rbranch']}' and transaction_food.email = user_acc.email '''
    )

    context['transaction_dict'] = []

    for data in command :
        dict = {}
        dict['name'] = f"{data[0]} {data[1]}"
        dict['datetime'] = data[2]
        dict['status'] = data[3]
        dict['url'] = f"{data[4]}+{data[2]}"
        dict['email'] = data[4]
        context['transaction_dict'].append(dict)

    return render(request, 'transaksi-pesanan.html', context)

def detail_transaksi_pesanan(request, email, datetime):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }

    # email = request.COOKIES.get('email')

    query = execute_sql (
    f''' select transaction.datetime, user_acc.fname, user_acc.lname, transaction.street, transaction.city, transaction.district, transaction.province, transaction_food.foodname, transaction.totalfood, transaction.totaldiscount, transaction.deliveryfee, transaction.totalprice, payment_method.name, payment_status.name, transaction_status.name, courier.email, courier.platenum, courier.vehicletype, courier.vehiclebrand, restaurant.street, restaurant.district, restaurant.province, restaurant.rname, restaurant.rbranch, transaction_food.note, transaction_food.amount
    
    from transaction, user_acc, transaction_food, restaurant, payment_method, payment_status, transaction_history, transaction_status, courier 
    
    where courier.email = transaction.courierid and transaction_history.tsid = transaction_status.id and transaction.email = transaction_history.email and transaction.datetime = transaction_history.datetime and payment_status.id = transaction.psid and payment_method.id = transaction.pmid and restaurant.rbranch = transaction_food.rbranch  and restaurant.rname = transaction_food.rname and transaction.email = user_acc.email and transaction.datetime = transaction_food.datetime and transaction.email = transaction_food.email and transaction.email = '{email}' and transaction.datetime = '{datetime}'  '''
   )

    command = query[0]

    context['datetime'] = command[0]
    context['name'] = f"{command[1]} {command[2]}"
    context['street'] = command[3]
    context['city'] = command[4]
    context['district'] = command[5]
    context['province'] = command[6]
    context['foodname'] = []

    for data in query :
        dict = {}
        dict['food'] = data[7]
        dict['note'] = data[24]
        dict['amount'] = data[25]
        context['foodname'].append(dict)

    context['totalfood'] = command[8]
    context['totaldiscount'] = command[9]
    context['deliveryfee'] = command[10]
    context['totalprice'] = command[11]
    context['payment_method'] = command[12]
    context['payment_status'] = command[13]
    context['transaction_status'] = command[14]
    context['courier_email'] = command[15]

    context['couriername'] = execute_sql(
        f''' select fname, lname from user_acc where email = '{context['courier_email']}' '''
    )

    context['couriername'] = f"{context['couriername'][0][0]} {context['couriername'][0][1]}"

    context['platenum'] = command[16]
    context['vehicletype'] = command[17]
    context['vehiclebrand'] = command[18]
    context['streetresto'] = command[19]
    context['cityresto'] = command[20]
    context['provinceresto'] = command[21]
    context['restoname'] = f"{command[22]} {command[23]}"

    
    print(command)

    return render(request, 'detail-transaksi-pesanan.html', context)

def action(request, email, datetime) :
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }

    command = execute_sql(
        f''' select transaction_status.name from transaction_history, transaction_status where transaction_history.email = '{email}' and transaction_history.datetime = '{datetime}' and transaction_history.tsid = transaction_status.id '''
    )[0][0]

    if command == "Menunggu konfirmasi restoran" :
        execute_sql(
            f''' update transaction_history set tsid = '0000000000000000000000001' where transaction_history.email = '{email}' and transaction_history.datetime = '{datetime}' '''
        )
        
    elif command == "Pesanan sedang dipersiapkan" :
        id_kurir = execute_sql(
            f''' select email from courier order by random() limit 1  '''
        )[0][0]

        execute_sql(
            f''' update transaction set courierid = '{id_kurir}' where transaction.email = '{email}' and transaction.datetime = '{datetime}'  '''
        )
        
        execute_sql(
            f''' update transaction_history set tsid = '0000000000000000000000002' where transaction_history.email = '{email}' and transaction_history.datetime = '{datetime}' '''
        )

    return redirect("sirest:transaksi_pesanan")

def tambah_kategori(request):
    return render(request, 'form-tambah-kategori.html')

