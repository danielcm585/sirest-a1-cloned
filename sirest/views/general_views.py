from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from sirest.models.admin_model import Admin
from sirest.models.customer_model import Customer
from sirest.models.restaurant_model import Restaurant
from sirest.models.courier_model import Courier
from sirest.utils import execute_sql
from sirest.models.restaurant_model import Restaurant
from sirest.models.courier_model import Courier
from sirest.models.admin_model import Admin
from sirest.models.transaction_actor_model import TransactionActor

def index(request):
    context = {
        'is_logged_in': bool(request.COOKIES.get('is_logged_in') == 'True'),
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }
    return render(request, 'general/index.html', context)

def dashboard(request):
    is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
    if (not is_logged_in): return index(request)

    
    ophours = []

    is_verified = True
    role = request.COOKIES.get('role')
    user = None

    if (role == 'Admin'):
        user = Admin(execute_sql(f"select * from admin where email = '{request.email}'")[0]).json()
    else:
        if (role == 'Pelanggan'): 
            user = Customer(execute_sql(f"select * from customer where email = '{request.email}';")[0]).json()
        elif (role == 'Restoran'):
            user = Restaurant(execute_sql(f"select * from restaurant where email = '{request.email}'")[0]).json()

            op_hours = execute_sql(
                f''' select day, starthours, endhours from restaurant_operating_hours where name = '{user['rname'].replace("'","''")}' and branch = '{user['rbranch'].replace("'","''")}' '''
            )

            for data in op_hours :
                dict = {}
                dict['day'] = data[0]
                dict['starthours'] = str(data[1])
                dict['endhours'] = str(data[2])        
                ophours.append(dict)    
            print(op_hours)

        elif (role == 'Kurir'):
            user = Courier(execute_sql(f"select * from courier where email = '{request.email}'")[0]).json()
            kurir_detail = execute_sql(f'''
                SELECT * from courier as c
                INNER JOIN transaction_actor as ta
                ON C.email = TA.email
                where C.email = '{user['email']}';
            ''')

            print(kurir_detail)
        # is_verified = (user['transactionactor']['adminid'] != None)
    if(role == 'Admin') :
        context = {
        'is_logged_in': is_logged_in,
        'name': request.COOKIES.get('name'),
        'role': role,
        'is_verified': is_verified,
        'user': user,
        }
    elif(role == 'Pelanggan') :
        context = {
        'is_logged_in': is_logged_in,
        'name': request.COOKIES.get('name'),
        'role': role,
        'is_verified': is_verified,
        'user': user,
        }
    elif(role == 'Restoran'):
        context = {
        'is_logged_in': is_logged_in,
        'name': request.COOKIES.get('name'),
        'role': role,
        'is_verified': is_verified,
        'user': user,
        'ophours' : ophours,
        }
    else:
        context = {
            'is_logged_in': is_logged_in,
            'name': request.COOKIES.get('name'),
            'role': role,
            'is_verified': is_verified,
            'user': user,
            'kurir_detail' : kurir_detail
        }
    return render(request, 'general/dashboard.html', context)

def detail_user(request):
    is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
    if (not is_logged_in): return index(request)
    context = {
        'is_logged_in': is_logged_in,
        'name': request.COOKIES.get('name'),
        'role': request.COOKIES.get('role'),
    }
    return render(request, 'general/detail-user.html', context)

def daftar_aktor_transaksi_api(request):
    email = request.COOKIES.get('email')
    def get():
        # Get all food categories
        # rows = execute_sql(f"select * from ((select ta.email, concat(u.fname, ' ', u.lname) as nama, 'Kurir' as Role \
        # from transaction_actor ta, user_acc u \
        # where exists (select email from courier c where c.email = ta.email) \
        # and ta.adminid = '{email}' and ta.email = u.email) \
        # union \
        # (select ta.email, concat(u.fname, ' ', u.lname) as nama, 'Pelanggan' as Role \
        # from transaction_actor ta, user_acc u \
        # where not exists (select email from courier c where c.email = ta.email) \
        # and ta.adminid = '{email}' and ta.email = u.email)) as hasil;")
        rows = execute_sql(f'''
            SELECT * from transaction_actor;
        ''')
        json = [ TransactionActor(row).json() for row in rows ]
        return JsonResponse(json, safe=False, status=200)

    if (request.method == 'GET'): return get()