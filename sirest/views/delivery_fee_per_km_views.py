from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.decorators import api_view
from sirest.forms import *
from sirest.views.general_views import *
from sirest.models.payment_method_model import PaymentMethod
from sirest.utils import execute_sql
from sirest.models.transaction_model import *
from django.core import serializers
from datetime import datetime
from django.db import connection
from collections import namedtuple


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def query(cmd):
    ret = []
    with connection.cursor() as cursor:
        # cursor.execute("SET SEARCH_PATH TO tk1_a1")

        try:
            cursor.execute(cmd)

            if cmd.lower()[0:6]=="select":
                ret = dictfetchall(cursor)
            else :
                ret = cursor.rowcount
        except Exception as e:
            ret = e

    return ret

def buat_tarif_pengiriman(request):
    # is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
    # role = request.COOKIES.get('role')
    # if (not is_logged_in): return index(request)
    # if (role != 'Admin'): return forbidden(request)
    # context = {
    #     'is_logged_in': is_logged_in,
    #     'name': request.COOKIES.get('name'),
    #     'role': role,
    # }

    # return render(request, 'admin/form-buat-tarif-pengiriman-per-km.html')



    # context = {
    #     'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
    #     'name': request.COOKIES.get('name'),
    #     'role': request.COOKIES.get('role'),
    # }

    # if request.method == "POST":
        
    #     provinsi = request.POST['provinsi']
    #     biayaMotor = request.POST['biayaMotor']
    #     biayaMobil = request.POST['biayaMobil']

    #     result = query("""SELECT id FROM DELIVERY_FEE_PER_KM""")
    #     id = result[len(result)-1]["id"]
    #     print(result)
    #     id = id[0] + str(int(id[1:])+1)

    #     execute_sql(f'''
    #         INSERT INTO DELIVERY_FEE_PER_KM values(
    #             '{id}', '{provinsi}', '{biayaMotor}', '{biayaMobil}' 
    #         );
    #     ''')
    
    #     return redirect('/daftar-tarif-pengiriman-per-km/')

    # return render(request, 'admin/form-buat-tarif-pengiriman-per-km.html', context)

    if request.method == "POST":
        provinsi = request.POST.get("provinsi")
        biayaMotor = request.POST.get("biayaMotor")
        biayaMobil = request.POST.get("biayaMobil")

        result = query("""SELECT id FROM DELIVERY_FEE_PER_KM""")
        print(result)
        id = result[len(result)-1]["id"]
        print(result)
        id = id[0] + str(int(id[1:])+1)

        result2 = query(f"""INSERT INTO DELIVERY_FEE_PER_KM VALUES ('{id}','{provinsi}', '{biayaMotor}', '{biayaMobil}')""")
        print(result2)

        return redirect('/daftar-tarif-pengiriman/')
    
        
    return render(request, 'admin/form-buat-tarif-pengiriman-per-km.html')


def daftar_tarif_pengiriman(request):

    # is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
    # role = request.COOKIES.get('role')
    # if (not is_logged_in): return index(request)
    # if (role != 'Admin'): return forbidden(request)
    # context = {
    #     'is_logged_in': is_logged_in,
    #     'name': request.COOKIES.get('name'),
    #     'role': role,
    # }

    # return render(request, 'admin/daftar-tarif-pengiriman-per-km.html')



    # data = {}
    # data['is_logged_in'] = bool(request.COOKIES.get('is_logged_in') == 'True')
    # data['role'] = request.COOKIES.get('role')
    # data['name'] = request.COOKIES.get('name')
    # daftar_tarif_pengiriman = []
    
    # rows_tarif_pengiriman = execute_sql(f'''
    #     SELECT * FROM DELIVERY_FEE_PER_KM;
    # ''')

    
    # for i in range(len(rows_tarif_pengiriman)):
    #     daftar_tarif_pengiriman.append({
    #         "pk" : rows_tarif_pengiriman[i][0],
    #         "provinsi" : rows_tarif_pengiriman[i][1],
    #         "biayaMotor" : rows_tarif_pengiriman[i][2],
    #         "biayaMobil" : rows_tarif_pengiriman[i][3]
    #     })
    
    # data["daftar_tarif_pengiriman"] = daftar_tarif_pengiriman

    # return render(request, 'admin/daftar-tarif-pengiriman-per-km.html', {"data" : data})

    result = query("""SELECT * FROM DELIVERY_FEE_PER_KM""")
    print(result)

    # for tarif_pengiriman in result:
    #     provinsi = query(
    #         f"""SELECT * FROM DELIVERY_FEE_PER_KM WHERE id ='{tarif_pengiriman['id']}' """)
        # if len(provinsi) == 0:
        #     tarif_pengiriman['jenis'] = 'Special day'
        # else:
        #     promo['jenis'] = 'Min transaction'

    context = {'tarif_pengiriman': result}
    return render(request, "daftar-tarif-pengiriman-per-km.html", context)


def ubah_tarif_pengiriman(request, pk):
    # return render(request, 'admin/ubah-tarif-pengiriman-per-km.html')



    data = {}
    data['is_logged_in'] = bool(request.COOKIES.get('is_logged_in') == 'True')
    data['role'] = request.COOKIES.get('role')
    data['name'] = request.COOKIES.get('name')

    rows = execute_sql(f'''

        SELECT * FROM DELIVERY_FEE_PER_KM
        WHERE Id = '{pk}';
        ''')[0]
    
    provinsi = {
        "nama" : rows[1]
    }

    data["provinsi"] = provinsi

    if request.method != "POST":
        return render(request, 'admin/ubah-tarif-pengiriman-per-km.html', {'data' : data})

    body = request.POST.get
    biayaMotor = body('biayaMotor', False)
    biayaMobil = body('biayaMobil', False)

    execute_sql(f'''
        UPDATE DELIVERY_FEE_PER_KM
        SET MotorbikeFee = {biayaMotor}
        WHERE id = '{pk}';
    ''')

    execute_sql(f'''
        UPDATE DELIVERY_FEE_PER_KM
        SET CarFee = {biayaMobil}
        WHERE id = '{pk}'
    ''')

    return redirect('/daftar-tarif-pengiriman-per-km')


def hapus_tarif_pengiriman(request, id):
    # execute_sql(f'''
    #     DELETE FROM DELIVERY_FEE_PER_KM
    #     WHERE id = '{pk}'
    # ''')
    # return redirect('/daftar-tarif-pengiriman-per-km')

    
    # result_3 = query(f"""delete from restaurant_promo where pid = '{id_promo}'""")
    # result_2 = query(f"""delete from special_day_promo where id_special_day_promo = '{id_promo}'""")
    # result_1 = query(f"""delete from min_transaction_promo where id_min_transaction_promo = '{id_promo}'""")

    result = query(f"""delete from DELIVERY_FEE_PER_KM where id = '{id}'""")

    return redirect('/daftar-tarif-pengiriman')

