from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from sirest.models.food_category_model import FoodCategory
from sirest.forms.food_category_form import FoodCategoryForm
from sirest.utils import execute_sql

def food_category(request):
    is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
    role = request.COOKIES.get('role')
    if (not is_logged_in): return index(request)
    if (role != 'Admin'): return forbidden(request)
    context = {
        'is_logged_in': is_logged_in,
        'name': request.COOKIES.get('name'),
        'role': role,
    }
    return render(request, 'admin/food-category.html', context)

def new_food_category(request):
    is_logged_in = bool(request.COOKIES.get('is_logged_in') == 'True')
    role = request.COOKIES.get('role')
    if (not is_logged_in): return index(request)
    if (role != 'Admin'): return forbidden(request)
    context = {
        'is_logged_in': is_logged_in,
        'name': request.COOKIES.get('name'),
        'role': role,
    }
    return render(request, 'admin/new-food-category.html', context)

@api_view(['GET','POST'])
def food_category_api(request):
    def get():
        # Get all food categories
        rows = execute_sql("select * from food_category;")
        json = [ FoodCategory(row).json() for row in rows ]
        return JsonResponse(json, safe=False, status=200)

    def post():
        # Create new food category
        form = FoodCategoryForm(request.POST)
        
        if (form.is_valid()):
            rows = execute_sql("select id from food_category order by id desc;")
            if (len(rows) > 0): id = str(int(rows[0][0])+1).rjust(20,'0')
            else: id = '0'*20
            name = form.cleaned_data.get('name')

            execute_sql(f"insert into food_category values ('{id}','{name}');")

            return JsonResponse({ 'message': 'Kategori makanan baru berhasil disimpan' }, status=200)
        return JsonResponse({ 'message': 'Input invalid' }, status=400)

    if (request.method == 'GET'): return get()
    elif (request.method == 'POST'): return post()

@api_view(['DELETE'])
def food_category_id_api(request, id):
    def delete():
        # Delete food category :id
        execute_sql(f"delete from food_category where id = '{id}';")
        return JsonResponse({ 'message': 'Kategori makanan dihapus' }, status=200)

    if (request.method == 'DELETE'): return delete()