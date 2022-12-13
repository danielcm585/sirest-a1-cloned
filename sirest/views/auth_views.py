from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from sirest.forms.admin_form import AdminForm
from sirest.forms.courier_form import CourierForm
from sirest.forms.customer_form import CustomerForm
from sirest.forms.restaurant_form import RestaurantForm
from sirest.forms.user_form import UserForm
from sirest.models.user_model import User
from sirest.models.transaction_model import Transaction
from sirest.utils import execute_sql

def login(request):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }
    return render(request, 'general/login.html', context)
    
def register(request):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }
    return render(request, 'general/register.html', context)

def forbidden(request):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }
    return render(request, 'general/forbidden.html', context)

def register_admin_api(request):
    form = AdminForm(request.POST)

    if (form.is_valid()):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        name = form.cleaned_data.get('name')
        fname = name.split()[0]
        lname = name.split()[1]
        phonenum = form.cleaned_data.get('phonenum')

        execute_sql(f"insert into user_acc values ('{email}','{password}','{phonenum}','{fname}','{lname}');")
        execute_sql(f"insert into admin values ('{email}');")

        return JsonResponse({ 'message': 'Akun admin berhasil dibuat' }, status=200)
    return JsonResponse({ 'message': 'Input invalid' }, status=400)

def register_customer_api(request):
    form = CustomerForm(request.POST)

    if (form.is_valid()):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        name = form.cleaned_data.get('name')
        fname = name.split()[0]
        lname = name.split()[1]
        phonenum = form.cleaned_data.get('phonenum')
        nik = form.cleaned_data.get('nik')
        bankname = form.cleaned_data.get('bankname')
        accountno = form.cleaned_data.get('accountno')
        birthdate = form.cleaned_data.get('birthdate')
        sex = form.cleaned_data.get('sex')

        execute_sql(f"insert into user_acc values ('{email}','{password}','{phonenum}','{fname}','{lname}');")
        execute_sql(f"""
            insert into transaction_actor (email, nik, bankname, accountno) values 
                ('{email}','{nik}','{bankname}','{accountno}');
        """)
        execute_sql(f"insert into customer values ('{email}','{birthdate}','{sex}');")

        return JsonResponse({ 'message': 'Akun pelanggan berhasil dibuat' }, status=200)
    return JsonResponse({ 'message': 'Input invalid' }, status=400)

def register_restaurant_api(request):
    form = RestaurantForm(request.POST)

    if (form.is_valid()):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        name = form.cleaned_data.get('name')
        fname = name.split()[0]
        lname = name.split()[1]
        phonenum = form.cleaned_data.get('phonenum')
        nik = form.cleaned_data.get('nik')
        bankname = form.cleaned_data.get('bankname')
        accountno = form.cleaned_data.get('accountno')
        rname = form.cleaned_data.get('rname')
        rbranch = form.cleaned_data.get('rbranch')
        rphonenum = form.cleaned_data.get('rphonenum')
        street = form.cleaned_data.get('street')
        district = form.cleaned_data.get('district')
        city = form.cleaned_data.get('city')
        province = form.cleaned_data.get('province')
        rcategory = form.cleaned_data.get('rcategory')
        
        execute_sql(f"insert into user_acc values ('{email}','{password}','{phonenum}','{fname}','{lname}');")
        execute_sql(f"""
            insert into transaction_actor (email, nik, bankname, accountno) values 
                ('{email}','{nik}','{bankname}','{accountno}');
        """)
        execute_sql(f"""
            insert into restaurant (rname, rbranch, email, rphonenum, street, district, city, province, rcategory) values 
                ('{rname}','{rbranch}','{email}','{rphonenum}','{street}','{district}','{city}','{province}','{rcategory}');
        """)

        return JsonResponse({ 'message': 'Akun restoran berhasil dibuat' }, status=200)
    return JsonResponse({ 'message': 'Input invalid' }, status=400)

def register_courier_api(request):
    form = RestaurantForm(request.POST)

    if (form.is_valid()):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        name = form.cleaned_data.get('name')
        fname = name.split()[0]
        lname = name.split()[1]
        phonenum = form.cleaned_data.get('phonenum')
        nik = form.cleaned_data.get('nik')
        bankname = form.cleaned_data.get('bankname')
        accountno = form.cleaned_data.get('accountno')
        platenum = form.cleaned_data.get('platenum')
        drivinglicensenum = form.cleaned_data.get('drivinglicensenum')
        vechicletype = form.cleaned_data.get('vechicletype')
        vehiclebrand = form.cleaned_data.get('vehiclebrand')
        
        execute_sql(f"insert into user_acc values ('{email}','{password}','{phonenum}','{fname}','{lname}');")
        execute_sql(f"""
            insert into transaction_actor (email, nik, bankname, accountno) values 
                ('{email}','{nik}','{bankname}','{accountno}');
        """)
        execute_sql(f"insert into courier values ('{email}','{platenum}','{vechicletype}','{vehiclebrand}');")

        return JsonResponse({ 'message': 'Akun kurir berhasil dibuat' }, status=200)
    return JsonResponse({ 'message': 'Input invalid' }, status=400)

def login_api(request):
    form = UserForm(request.POST)
    if (form.is_valid()):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        
        rows = execute_sql(f"select * from user_acc where email = '{email}';")
        
        if (len(rows) != 0):
            user = User(rows[0])
            
            if (password == user.password):
                is_admin = (len(execute_sql(f"select * from admin where email = '{user.email}';")) > 0)
                is_courier = (len(execute_sql(f"select * from courier where email = '{user.email}';")) > 0)
                is_customer = (len(execute_sql(f"select * from customer where email = '{user.email}';")) > 0)
                is_restaurant = (len(execute_sql(f"select * from restaurant where email = '{user.email}';")) > 0)

                session_id = str(execute_sql("select count(*) from session;")[0][0]+1).rjust(20,'0')
                execute_sql(f"insert into session (id, email, opened_at) values ('{session_id}','{email}','{datetime.now()}');")

                response = JsonResponse({ 'message': 'Login berhasil' }, status=200)

                response.set_cookie('is_logged_in', 'True')
                response.set_cookie('session_id', session_id)
                response.set_cookie('name', f'{user.fname} {user.lname}')
                response.set_cookie('email', f'{user.email}')
                

                if (is_admin): response.set_cookie('role', 'Admin')
                elif (is_courier): response.set_cookie('role', 'Kurir')
                elif (is_customer): response.set_cookie('role', 'Pelanggan')
                elif (is_restaurant): response.set_cookie('role', 'Restoran')
                else: print('Loh kok bisa?')

                return response
            return JsonResponse({ 'message': 'Password salah' }, status=400)
        return JsonResponse({ 'message': 'User tidak ditemukan' }, status=400)
    return JsonResponse({ 'message': 'Input invalid' }, status=400)
        
def logout_api(request):
    session_id = request.COOKIES.get('session_id')
    execute_sql(f"update session set closed_at = '{datetime.now()}' where id = '{session_id}';")

    response = JsonResponse({ 'message': 'Logout berhasil' }, status=200)
    
    response.delete_cookie("is_logged_in")
    response.delete_cookie("session_id")
    response.delete_cookie("name")
    response.delete_cookie("role")

    return response

def test(request):
    # dict = {
    #     'test': 'test',
    #     'UwU': {
    #         'UwU': 'UwU'
    #     }
    # }
    # print(dict['UwU'])
    # context = {
    #     'data': dict
    # }
    # return render(request, 'general/test.html', context)

    rows = execute_sql("""
        select * from transaction as t where exists (
            select * from transaction_history as th where 
            t.email = th.email and t.datetime = th.datetime and 
            th.tsid in ('0000000000000000000000004','0000000000000000000000005')
        );
    """)
    transactions = [ Transaction(row).json() for row in rows ]
    return JsonResponse(transactions, safe=False, status=200)
