from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from sirest.views.auth_views import *
from sirest.utils import *
from rest_framework.decorators import api_view
from sirest.forms.trigger_5_form import *
from sirest.models.resto_category_model import RestoCategory
from sirest.models.ingredient_model import BahanMakanan
from sirest.models.courier_ongoing_model import *

def daftar_ingredient(request):
    is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
    role = request.COOKIES.get('role')
    if (not is_logged_in): return index(request)
    if (role != 'Admin'): return forbidden(request)
    context = {
        'is_logged_in': is_logged_in,
        'name': request.COOKIES.get('name'),
        'role': role,
    }
    return render(request, 'admin/bahan-makanan.html', context)

@api_view(['GET','POST'])
def ingredients_api(request):
    def get():
        # Get all food categories
        rows = execute_sql("select * from ingredient;")
        json = [ BahanMakanan(row).json() for row in rows ]
        return JsonResponse(json, safe=False, status=200)

    def post():
        # Create new food category
        form = IngredientForm(request.POST)
        
        if (form.is_valid()):
            id = str(execute_sql("select count(*) from ingredient;")[0][0]+1).rjust(20,'0')
            name = form.cleaned_data.get('name')

            execute_sql(f"insert into ingredient values ('{id}','{name}');")

            return JsonResponse({ 'message': 'Berhasil menambah bahan makanan baru' }, status=200)
        return JsonResponse({ 'message': 'Input invalid' }, status=400)

    if (request.method == 'GET'): return get()
    elif (request.method == 'POST'): return post()

@api_view(['DELETE'])
def ingredient_id_api(request, id):
    def delete():
        # Delete resto category :id
        execute_sql(f"delete from ingredient where id = '{id}';")
        return JsonResponse({ 'message': 'Bahan makanan dihapus' }, status=200)

    if (request.method == 'DELETE'): return delete()

def tambah_ingredient(request):
    is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
    role = request.COOKIES.get('role')
    if (not is_logged_in): return index(request)
    if (role != 'Admin'): return forbidden(request)
    context = {
        'is_logged_in': is_logged_in,
        'name': request.COOKIES.get('name'),
        'role': role,
    }
    return render(request, 'admin/tambah-bahan-makanan.html', context)

def daftar_kategori_restoran(request):
    is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
    role = request.COOKIES.get('role')
    if (not is_logged_in): return index(request)
    if (role != 'Admin'): return forbidden(request)
    context = {
        'is_logged_in': is_logged_in,
        'name': request.COOKIES.get('name'),
        'role': role,
    }
    return render(request, 'admin/restaurant-category.html', context)

@api_view(['GET','POST'])
def resto_category_api(request):
    def get():
        # Get all food categories
        rows = execute_sql("select * from restaurant_category;")
        json = [ RestoCategory(row).json() for row in rows ]
        return JsonResponse(json, safe=False, status=200)

    def post():
        # Create new food category
        form = RestoCategoryForm(request.POST)
        
        if (form.is_valid()):
            id = str(execute_sql("select count(*) from restaurant_category;")[0][0]+1).rjust(20,'0')
            name = form.cleaned_data.get('name')

            execute_sql(f"insert into restaurant_category values ('{id}','{name}');")

            return JsonResponse({ 'message': 'Berhasil membuat kategori restoran baru' }, status=200)
        return JsonResponse({ 'message': 'Input invalid' }, status=400)

    if (request.method == 'GET'): return get()
    elif (request.method == 'POST'): return post()

@api_view(['DELETE'])
def resto_category_id_api(request, id):
    def delete():
        # Delete resto category :id
        execute_sql(f"delete from restaurant_category where id = '{id}';")
        return JsonResponse({ 'message': 'Kategori restoran dihapus' }, status=200)

    if (request.method == 'DELETE'): return delete()

def tambah_kategori_restoran(request):
    is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
    role = request.COOKIES.get('role')
    if (not is_logged_in): return index(request)
    if (role != 'Admin'): return forbidden(request)
    context = {
        'is_logged_in': is_logged_in,
        'name': request.COOKIES.get('name'),
        'role': role,
    }
    return render(request, 'admin/tambah-kategori-restoran.html', context)

def kurir_pesanan_berlangsung(request):
    is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
    role = request.COOKIES.get('role')
    if (not is_logged_in): return index(request)
    if (role != 'Kurir'): return forbidden(request)
    context = {
        'is_logged_in': is_logged_in,
        'name': request.COOKIES.get('name'),
        'role': role,
        'email' : request.COOKIES.get('email')
    }
    return render(request, 'kurir/pesanan-berlangsung.html', context)

@api_view(['GET','POST'])
def kurir_ongoing_order_api(request):
    email = str(request.COOKIES.get('email'))
    def get():
        # Get all food categories
        rows = execute_sql(f"select concat(tf.rname, ' ', tf.rbranch) as restoname, \
                            concat(u.fname, ' ', u.lname) as nama_pelanggan, th.datetime, ts.name, t.email \
                            from transaction_history th, \
                            transaction_food tf, transaction_status ts, transaction t, user_acc u where th.tsid = ts.id and \
                            tf.email = th.email and th.email = t.email and t.email = u.email and t.courierid = '{email}';")
        json = [CourierOngoingOrder(row).json() for row in rows ]
        return JsonResponse(json, safe=False, status=200)

    # def post():
    #     # Create new food category
    #     form = IngredientForm(request.POST)
        
    #     if (form.is_valid()):
    #         id = str(execute_sql("select count(*) from ingredient;")[0][0]+1).rjust(20,'0')
    #         name = form.cleaned_data.get('name')

    #         execute_sql(f"insert into ingredient values ('{id}','{name}');")

    #         return JsonResponse({ 'message': 'Berhasil menambah bahan makanan baru' }, status=200)
    #     return JsonResponse({ 'message': 'Input invalid' }, status=400)

    if (request.method == 'GET'): return get()
    # elif (request.method == 'POST'): return post()

def detail_pesanan_berlangsung(request):
    is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
    role = request.COOKIES.get('role')
    if (not is_logged_in): return index(request)
    if (role != 'Kurir'): return forbidden(request)
    context = {
        'is_logged_in': is_logged_in,
        'name': request.COOKIES.get('name'),
        'role': role,
    }
    return render(request, 'kurir/detail-pesanan-berlangsung.html', context)

def detail_pesanan_berlangsung_api(request, email, date):
    def get():
        # Get all food categories
        daftarpesanan = execute_sql(f"select foodname, amount from transaction_food where email = '{email} and datetime = {date};")
        namapemesan = execute_sql(f"select concat(fname, ' ', lname) as nama_pelanggan from user_acc where email = '{email}';")
        pesananinjson = [PesananMakanan(pesanan).json for pesanan in daftarpesanan]
        rows = execute_sql(f"select * from(select t.street, t.district, t.city, t.province, \
        concat(tf.rname, ' ', tf.rbranch) as restoname, r.street, r.district, r.city, r.province, \
        t.totalfood, t.totaldiscount, t.deliveryfee, t.totalprice, pm.name, ps.name,ts.name, \
        concat(u.fname, ' ', u.lname) as nama_kurir, c.platenum, c.vehicletype, c.vehiclebrand, t.courierid from transaction as t \
        inner join transaction_food as tf on t.email = tf.email and t.datetime = tf.datetime \
        inner join transaction_history as th on t.email = th.email and t.datetime = th.datetime \
        inner join payment_method pm on t.pmid = pm.id \
        inner join payment_status ps on t.psid = ps.id \
        inner join transaction_status ts on th.tsid = ts.id \
        inner join courier c on t.courierid = c.email \
        inner join user_acc u on u.email = t.courierid \
        inner join restaurant r on r.rname = tf.rname and r.rbranch = tf.rbranch) as h \
        where h.courierid = 'Dulce_Bashirian@gmail.com';")
        json = DetailPesanan(rows)
        json.waktuorder = date
        json.daftarpesanan = pesananinjson
        json.namapemesan = namapemesan
        jsonreturn = json.json()
        return JsonResponse(jsonreturn, safe=False, status=200)
    
    if (request.method == 'GET'): return get()