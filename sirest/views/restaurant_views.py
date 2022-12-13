from django.http import JsonResponse
from rest_framework.decorators import api_view
from sirest.models.food_model import Food
from sirest.models.restaurant_model import Restaurant
from sirest.utils import execute_sql

def restaurant_api(request):
    def get():
        # Get all restaurants
        rows = execute_sql(f"select * from restaurant;")
        json = [ Restaurant(row).json() for row in rows ]
        return JsonResponse(json, safe=False, status=200)

    def post():
        # Create new restaurant
        pass
    
    if (request.method == 'GET'): return get()
    elif (request.method == 'POST'): return post()

@api_view(['GET'])
def restaurant_menu_api(request, rname, rbranch):
    def get():
        # Get all menu from restaurant :id
        rows = execute_sql(f"select * from food where rname = '{rname}' and rbranch = '{rbranch}';")
        json = [ Food(row).json() for row in rows ]
        return JsonResponse(json, safe=False, status=200)

    if (request.method == 'GET'): return get()