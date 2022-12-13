from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from sirest.forms import *

def buat_makanan(request):
    return render(request, 'general/form-buat-makanan.html')

def daftar_makanan(request):
    return render(request, 'general/daftar-makanan.html')

def daftar_restoran_dan_makanan(request):
    return render(request, 'general/daftar-restoran-dan-makanan.html')

def detail_restoran(request):
    return render(request, 'general/detail-restoran.html')

def menu_restoran(request):
    return render(request, 'general/menu-restoran.html')

def ubah_makanan(request):
    return render(request, 'general/ubah-makanan.html')