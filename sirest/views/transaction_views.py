import random
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from sirest.models.transaction_model import Transaction
from sirest.models.customer_model import Customer
from sirest.utils import execute_sql

def transaction(request):
    is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
    role = request.COOKIES.get('role')
    if (not is_logged_in): return index(request)
    if (role != 'Pelanggan'): return forbidden(request)

    is_verified = True
    role = request.COOKIES.get('role')
    session_id = request.POST.get('session_id')
    user = Customer(execute_sql(f"select * from customer where email = '{request.email}';")[0]).json()
    is_verified = (user['transactionactor']['adminid'] != None)
    
    context = {
        'is_logged_in': is_logged_in,
        'name': request.COOKIES.get('name'),
        'role': role,
        'is_verified': is_verified,
    }
    return render(request, 'customer/transaction.html', context)
    
def transaction_detail(request, email, date):
    is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
    role = request.COOKIES.get('role')
    if (not is_logged_in): return index(request)
    if (role != 'Pelanggan' or email != request.email): return forbidden(request)

    is_verified = True
    role = request.COOKIES.get('role')
    session_id = request.POST.get('session_id')
    user = Customer(execute_sql(f"select * from customer where email = '{request.email}';")[0]).json()
    is_verified = (user['transactionactor']['adminid'] != None)
    
    context = {
        'is_logged_in': is_logged_in,
        'name': request.COOKIES.get('name'),
        'role': role,
        'email': email,
        'date': date,
        'is_verified': is_verified,
    }
    return render(request, 'customer/transaction-detail.html', context)

def transaction_review(request, email, date):
    is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
    role = request.COOKIES.get('role')
    if (not is_logged_in): return index(request)
    if (role != 'Pelanggan' or email != request.email): return forbidden(request)

    is_verified = True
    role = request.COOKIES.get('role')
    session_id = request.POST.get('session_id')
    user = Customer(execute_sql(f"select * from customer where email = '{request.email}';")[0]).json()
    is_verified = (user['transactionactor']['adminid'] != None)

    context = {
        'is_logged_in': is_logged_in,
        'name': request.COOKIES.get('name'),
        'role': role,
        'email': email,
        'date': date,
        'is_verified': is_verified,
    }
    return render(request, 'customer/transaction-review.html', context)

def transaction_payment(request, email, date):
    is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
    role = request.COOKIES.get('role')
    if (not is_logged_in): return index(request)
    if (role != 'Pelanggan' or email != request.email): return forbidden(request)

    is_verified = True
    role = request.COOKIES.get('role')
    session_id = request.POST.get('session_id')
    user = Customer(execute_sql(f"select * from customer where email = '{request.email}';")[0]).json()
    is_verified = (user['transactionactor']['adminid'] != None)

    context = {
        'is_logged_in': is_logged_in,
        'name': request.COOKIES.get('name'),
        'role': role,
        'email': email,
        'date': date,
        'is_verified': is_verified,
    }
    return render(request, 'customer/transaction-payment.html', context)

def new_transaction(request, step):
    is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
    role = request.COOKIES.get('role')
    if (not is_logged_in): return index(request)
    if (role != 'Pelanggan'): return forbidden(request)

    is_verified = True
    role = request.COOKIES.get('role')
    session_id = request.POST.get('session_id')
    user = Customer(execute_sql(f"select * from customer where email = '{request.email}';")[0]).json()
    is_verified = (user['transactionactor']['adminid'] != None)

    context = { 
        'is_logged_in': is_logged_in,
        'name': request.COOKIES.get('name'),
        'role': role,
        'step': step,
        'is_verified': is_verified,
    }
    return render(request, 'customer/new-transaction.html', context)

@csrf_exempt
def transaction_api(request):
    def get():
        # Get all transactions
        rows = execute_sql(f"select * from transaction where email = '{request.email}' order by datetime;")
        json = [ Transaction(row).json() for row in rows ]
        
        def filter_ongoing(transaction):
            if (transaction['transactionstatus'] == None): return False
            size = len(transaction['transactionstatus'])
            return size > 0 and transaction['transactionstatus'][size-1]['statusid'] <= '0000000000000000000000003'

        json = list(filter(filter_ongoing, json))
        return JsonResponse(json, safe=False, status=200)

    def post():
        # Create new transaction]]
        email = request.email
        date = str(datetime.now())[:19]
        street = request.POST.get('street')
        district = request.POST.get('district')
        city = request.POST.get('city')
        province = request.POST.get('province')
        pmid = request.POST.get('pmid')
        psid = '0'*25
        dfid = execute_sql(f"select id from delivery_fee_per_km where province = '{province}';")[0][0]
        courierType = request.POST.get('courierType')
        courierId = random.choice([ 
            row[0] for row in execute_sql(f"""
                select email from courier where vehicletype = '{courierType}';
            """) 
        ])
        orders = request.POST.get('orders')
        rname = request.POST.get('rname')
        rbranch = request.POST.get('rbranch')

        execute_sql(f"""
            insert into transaction (email, datetime, street, district, city, province, totalfood, totaldiscount, deliveryfee, totalprice, pmid, psid, dfid, courierId) values
                ('{email}', '{date}', '{street}', '{district}', '{city}', '{province}', 0, 0, 0, 0, '{pmid}', '{psid}', '{dfid}', '{courierId}');
        """)
        execute_sql(f"insert into transaction_history values ('{email}', '{date}', '0000000000000000000000000', '{date}')")

        for i in range(100):
            try:
                foodname = request.POST.get(f"orders[{i}][foodname]")
                amount = request.POST.get(f"orders[{i}][amount]")
                note = request.POST.get(f"orders[{i}][note]")

                execute_sql(f"""
                    insert into transaction_food values 
                        ('{email}','{date}','{rname}','{rbranch}','{foodname}','{amount}','{note}');
                """)
            except:
                print(f"error {i}")
                break

        new_transaction = Transaction(execute_sql(f"select * from transaction where email = '{email}' and datetime = '{date}';")[0])
        return JsonResponse(new_transaction.json(), status=200)

    if (request.method == 'GET'): return get()
    elif (request.method == 'POST'): return post()

@csrf_exempt
def transaction_id_api(request, email, date):
    def get():
        # Get details of transaction :id
        if (email == request.email):
            rows = execute_sql(f"select * from transaction where email = '{email}' and datetime = '{date}';")
            transaction = Transaction(rows[0])
            return JsonResponse(transaction.json(), status=200)
        return JsonResponse({ 'message': 'Anda bukan pemiilik transaksi' }, status=400)

    def post():
        # Update transaction :id status 
        if (email == request.email):
            print(request.POST)
            payment_status = request.POST.get('paymentstatus')
            if (payment_status != None):
                psid = execute_sql(f"select id from payment_status where name = '{payment_status}';")[0][0]
                execute_sql(f"update transaction set psid = '{psid}' where email = '{email}' and datetime = '{date}';")

            transaction_status = request.POST.get('transactionstatus')
            print(transaction_status)
            if (transaction_status != None):
                now = str(datetime.now())[:19]
                tsid = execute_sql(f"select id from transaction_status where name = '{transaction_status}';")[0][0]
                execute_sql(f"insert into transaction_history values ('{email}','{date}','{tsid}','{now}')")

            rows = execute_sql(f"select * from transaction where email = '{email}' and datetime = '{date}';")
            transaction = Transaction(rows[0])
            return JsonResponse(transaction.json(), status=200)
        return JsonResponse({ 'message': 'Anda bukan pemiilik transaksi' }, status=400)

    if (request.method == 'GET'): return get()
    elif (request.method == 'POST'): return post()
