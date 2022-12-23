from django.urls import path
from sirest.forms.restopay_form import restopay
from sirest.views.general_views import *
from sirest.views.auth_views import *
from sirest.views.jam_op_views import daftar_jam_op, jam_op, jam_op_api, pilih_jam_op, tambah_jam_op, ubah_jam_op, hapus_jam_op
from sirest.views.restopay_views import isi_restopay, tarik_restopay, read_restopay
from sirest.views.transaction_views import *
from sirest.views.food_category_views import *
from sirest.views.other_views import *
from sirest.views.delivery_fee_per_km_views import *
from sirest.views.food_views import *
from sirest.views.trigger_5_views import *
from sirest.views.restaurant_views import *

app_name = 'sirest'

urlpatterns = [
    # General
    path('', index, name='index'),
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/user-detail', detail_user, name='detail_user'),
    path('api/test/', test, name='test'),
    path('api/dashboard/admin', daftar_aktor_transaksi_api, name='daftar_transaksi_aktor'),

    # Auth
    path('login/', login, name='login'),
    path('register/', register, name='register'),

    path('api/login/', login_api, name='login_api'),
    path('api/logout/', logout_api, name='logout_api'),
    path('api/verify/<str:id>/', verify_user_api, name='verify_user_api'),
    path('api/register/pelanggan/', register_customer_api, name='register_customer_api'),
    path('api/register/admin/', register_admin_api, name='register_admin_api'),
    path('api/register/restoran/', register_restaurant_api, name='register_restaurant_api'),
    path('api/register/kurir/', register_courier_api, name='register_courier_api'),

    # Food Category
    path('food-category/', food_category, name='food_category'),
    path('new-food-category/', new_food_category, name='new_food_category'),
    
    path('api/food-category/', food_category_api, name='food_category_api'),
    path('api/food-category/<str:id>/', food_category_id_api, name='food_category_id_api'),

    # Transaction
    path('transaction/', transaction, name='transaction'),
    path('transaction/<str:email>/<str:date>/', transaction_detail, name='transaction_detail'),
    path('new-transaction/<int:step>/', new_transaction, name='new_transaction'),
    path('transaction-review/<str:email>/<str:date>/', transaction_review, name='transaction_review'),
    path('transaction-payment/<str:email>/<str:date>/', transaction_payment, name='transaction_payment'),
    
    path('api/transaction/', transaction_api, name='transaction_api'),
    path('api/transaction/<str:email>/<str:date>/', transaction_id_api, name='transaction_id_api'),

    # Restaurant
    path('api/restaurant/', restaurant_api, name='restaurant_api'),
    path('api/restaurant-menu/<str:rname>/<str:rbranch>/', restaurant_menu_api, name='restaurant_menu_api'), 

    # Payment Method
    path('api/payment-method/', payment_method_api, name='payment_method_api'),

    #Ingredient
    path('bahan-makanan/', daftar_ingredient, name='bahan_makanan'),
    path('bahan-makanan/create/', tambah_ingredient, name='create_bahan_makanan'),
    path('api/bahan-makanan/', ingredients_api, name='ingredients_api'),
    path('api/bahan-makanan/<str:id>/', ingredient_id_api, name='ingredient_id_api'),

    #Restaurant category
    path('kategori-restoran/', daftar_kategori_restoran, name='kategori_resto'),
    path('kategori-restoran/create/', tambah_kategori_restoran, name='create_kategori_resto'),
    path('api/kategori-restoran/', resto_category_api, name='resto_category_api'),
    path('api/kategori-restoran/<str:id>/', resto_category_id_api, name='resto_category_id_api'),
    
    #Kurir
    path('pesanan-berlangsung/kurir/', kurir_pesanan_berlangsung, name='kurir_pesanan_berlangsung'),
    path('api/pesanan-berlangsung/kurir/', kurir_ongoing_order_api, name='kurir_pesanan_berlangsung_api'),
    path('pesanan-berlangsung/kurir/detail/', detail_pesanan_berlangsung, name='detail_pesanan_berlangsung'),
    path('api/pesanan-berlangsung/kurir/detail/<str:email>/<str:date>', detail_pesanan_berlangsung_api, name='detail_pesanan_berlangsung_api'), 

    # Riwayat Pesanan
    path('riwayat-transaksi-pesanan/', riwayat_transaksi_pesanan_api, name='riwayat_transaksi_pesanan'),
    path('riwayat-detail/<str:email>/<str:datetime>/', riwayat_detail, name='riwayat_detail'), 


    #Other
    path('food/', food, name='food'),

    #promo stuff (carlene)
    path('form-nilai/<str:email>/<str:datetime>/', nilai_pesanan, name='nilai_pesanan'), 
    path('buat-promo/', pilih_promo, name='pilih_promo'),
    path('form-minimum-transaksi/', promo_minimum_transaksi, name='promo_minimum_transaksi'),
    path('form-hari-spesial/', promo_hari_spesial, name='promo_hari_spesial'),
    path('promo/', promo, name='promo'),
    path('daftar-promo/', daftar_promo, name='daftar_promo'),
    path('detail-promo-hs/<pk>', detail_promo_hs, name='detail_promo_hs'),
    path('detail-promo-min/<pk>', detail_promo_min, name='detail_promo_min'),
    path('ubah-promo-min/<pk>', ubah_promo_min, name='ubah_promo_min'),
    path('ubah-promo-hs/<pk>', ubah_promo_hs, name='ubah_promo_min'),
    path('delete-promo/<pk>', delete_promo, name='delete_promo'),
    path('tambah-promo-restauran/', tambah_promo_resto, name='tambah_promo_resto'),
    path('daftar-promo-resto/', daftar_promo_restaurant, name='daftar_promo_restaurant'),
    path('detail-promo-resto/<pk>', detail_promo_resto, name='detail_promo_resto'),
    path('ubah-promo-resto/<pk>', ubah_promo_resto, name='ubah_promo_resto'),
    path('hapus-promo-resto/<pk>', hapus_promo_resto, name='hapus_promo_resto'),
    path('get-promo-detail/', get_promo_detail, name='get_promo_detail'),


    path('jam-op/', jam_op, name='jam-op'),
    path('buat-jam-op/', pilih_jam_op, name='pilih-jam-op'),
    path('daftar-jam-op/', daftar_jam_op, name='daftar-jam-op'),
    path('tambah-jam-op/', tambah_jam_op, name='tambah-jam-op'),
    path('ubah-jam-op/<str:id>', ubah_jam_op, name='ubah_jam_op'),
    path('hapus-jam-op/<str:id>', hapus_jam_op, name='hapus_jam_op'),


    path('api/jam-op/', jam_op_api, name='jam_op_api'),
    path('api/jam-op/<str:rname>/<str:rbranch>/<str:day>/', jam_op_api, name='jam_op_api'),
    path('api/transaction/<str:email>/<str:date>/', transaction_id_api, name='transaction_id_api'),

    path('restopay/', read_restopay, name='restopay'),
    path('isi-restopay/', isi_restopay, name='isi_restopay'),
    path('tarik-restopay/', tarik_restopay, name='tarik_restopay'),

    path('action/<str:email>/<str:datetime>/', action, name='action'),
    path('transaksi-pesanan/', transaksi_pesanan, name='transaksi_pesanan'),
    path('detail-transaksi-pesanan/<str:email>/<str:datetime>/', detail_transaksi_pesanan, name='detail_transaksi_pesanan'),

    path('buat-tarif-pengiriman/', buat_tarif_pengiriman, name='buat_tarif_pengiriman'),
    path('daftar-tarif-pengiriman/', daftar_tarif_pengiriman, name='daftar_tarif_pengiriman'),
    path('ubah-tarif-pengiriman/<pk>', ubah_tarif_pengiriman, name='ubah_tarif_pengiriman'),
    path('hapus-tarif-pengiriman/<str:id>', hapus_tarif_pengiriman, name='hapus_tarif_pengiriman'),
    path('buat-makanan/', buat_makanan, name='buat_makanan'),
    path('daftar-makanan/', daftar_makanan, name='daftar_makanan'),
    path('daftar-restoran-dan-makanan/', daftar_restoran_dan_makanan, name='daftar_restoran_dan_makanan'),
    path('detail-restoran/', detail_restoran, name='detail_restoran'),
    path('menu-restoran/', menu_restoran, name='menu_restoran'),
    path('ubah-makanan/', ubah_makanan, name='ubah_makanan'),
]