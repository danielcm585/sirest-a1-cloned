from django.http import JsonResponse
from rest_framework.decorators import api_view
from sirest.models.food_model import Food
from sirest.models.restaurant_model import Restaurant
from sirest.utils import execute_sql
from sirest.models.jamOp_model import Jam_op
from django.shortcuts import render, redirect
from sirest.forms.jam_op_form import JamOpForms

def jam_op (request) :
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }
    return render(request, 'crud-jam-op.html', context)
    
def daftar_jam_op(request):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }

    email = request.COOKIES.get('email')

    query = execute_sql(
        f''' select rname, rbranch from restaurant where email = '{email}' '''
    )

    context['rname'] = query[0][0]
    context['rbranch'] = query[0][1]

    op_hours = execute_sql(
        f''' select day, starthours, endhours from restaurant_operating_hours where name = '{ context['rname']}' and branch = '{context['rbranch']}' '''
    )

    context['op_hours_dict'] = []

    for data in op_hours :
        dict = {}
        dict['url'] = f"{context['rname']}+{context['rbranch']}+{data[0]}"
        dict['day'] = f"{data[0]}"
        dict['starthours'] = str(data[1])
        dict['endhours'] = str(data[2])
        context['op_hours_dict'].append(dict)

    print(context)

    return render(request, 'daftar-jam-op.html', context)

def pilih_jam_op(request):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }
    return render(request, 'pilih-jam-op.html',context)

def ubah_jam_op(request, id):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }

    id = id.split('+')

    command = execute_sql(
        f''' select starthours, endhours from restaurant_operating_hours where name = '{id[0]}' and branch = '{id[1]}' and day ='{id[2]}' '''
    ) 

    context['name'] = id[0]
    context['branch'] = id[1] 
    context['day'] = id[2]
    context['starthours'] = command[0][0]
    context['endhours'] = command[0][1]

    if request.method != 'POST' :
        return render(request, 'ubah-jam-op.html', context)
    
    starthours = request.POST["start"]
    endhours = request.POST["end"]

    execute_sql(
        f''' update restaurant_operating_hours set starthours = '{starthours}', endhours = '{endhours}' where name = '{id[0]}' and branch = '{id[1]}' and day ='{id[2]}'; '''
    )
    return redirect('sirest:daftar-jam-op')

def hapus_jam_op(request, id):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }

    id = id.split('+')

    execute_sql(
        f''' delete from restaurant_operating_hours where name = '{id[0]}' and branch = '{id[1]}' and day ='{id[2]}'; '''
    )
    return redirect('sirest:daftar-jam-op')

def tambah_jam_op(request):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }
    return render(request, 'tambah-jam-op.html', context)

def jam_op_api(request):
    user = Restaurant(execute_sql(f"select * from restaurant where email = '{request.email}'")[0]).json()
    is_verified = (user['transactionactor']['adminid'] != None)
    def get():
        # Get all operational hours
        rows = execute_sql(f"select * from restaurant_operating_hours;")
        json = [ Jam_op(row).json() for row in rows ]
        print(json)
        
        return JsonResponse(json, safe=False, status=200)

    def post():
        # Create new operational hours
        form = JamOpForms(request.POST)
        
        if (form.is_valid()):
            is_verified = True
            role = request.COOKIES.get('role')
            if role == 'Restoran' : 
                if is_verified :
                    execute_sql(f"insert into restaurant_operating_hours values ('{user['rname']}','{user['rbranch']}', '{form.cleaned_data['day']}', '{form.cleaned_data['starthours']}', '{form.cleaned_data['endhours']}');")
                    return JsonResponse({ 'message': 'Jam Operasional berhasil disimpan' }, status=200)
        return JsonResponse({ 'message': 'Input invalid' }, status = 400)

    if (request.method == 'GET'): return get()
    elif (request.method == 'POST'): return post()

def jam_op_id_api (request) :
        user = Restaurant(execute_sql(f"select * from restaurant where email = '{request.email}'")[0])
        def delete() :
            execute_sql(f"delete from restaurant_operating_hours where name = '{user.restaurant.name}' and branch = '{user.restaurant.branch}' and day = '{user.restaurant.day}';")
            return JsonResponse({ 'message': 'Jam Operasional berhasil disimpan' }, status=200)
        if (request.method == 'DELETE') : return delete()