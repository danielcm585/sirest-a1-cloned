from django.http import JsonResponse
from rest_framework.decorators import api_view
from sirest.models.food_model import Food
from sirest.models.transaction_actor_model import TransactionActor
from sirest.utils import execute_sql
from sirest.forms.restopay_form import restopay
from django.shortcuts import render, redirect


def read_restopay(request):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }
   
    email = request.COOKIES.get('email')
    
    
    restopay = execute_sql(
            f''' select restopay from sirest_a1.transaction_actor where email = '{email}' '''
        )[0][0]

    context['restopay'] = restopay

    print(context)

    return render(request, 'restopay.html', context)

def isi_restopay(request):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }
    email = request.COOKIES.get('email')
   
    command = execute_sql(
        f''' select restopay, bankname, accountno from transaction_actor where email = '{email}' '''
    )[0]

    context['restopay'] = command[0]
    context['bankname'] = command[1]
    context['accountno'] = command[2]


    if request.method != "POST" :
        return render(request, 'isi_restopay.html', context)

    nominal = int (request.POST["nominal"])
    print(nominal)
    print(email)
    

    command = execute_sql(
        f''' update sirest_a1.transaction_actor set restopay = {context['restopay']} + {nominal} where email = '{email}';  '''
    )

    return redirect('sirest:restopay')

def tarik_restopay(request):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }

    email = request.COOKIES.get('email')

    command = execute_sql(
        f''' select restopay, bankname, accountno from sirest_a1.transaction_actor where email = '{email}' '''
    )[0]

    context['restopay'] = command[0]
    context['bankname'] = command[1]
    context['accountno'] = command[2]

    if request.method != "POST" :
        return render(request, 'isi_restopay.html', context)

    nominal = int (request.POST["nominal"])

    command = execute_sql(
        f''' update transaction_actor set restopay = {context['restopay']} - {nominal} where email = '{email}';  '''
    )

    return redirect('sirest:restopay')
    
