from django import forms

class RestaurantForm(forms.Form):
    email = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)    
    name = forms.CharField(max_length=30)
    phonenum = forms.CharField(max_length=20)
    nik = forms.CharField(max_length=20)
    bankname = forms.CharField(max_length=20)
    accountno = forms.CharField(max_length=20)
    rname = forms.CharField(max_length=25)
    rbranch = forms.CharField(max_length=25)
    rphonenum = forms.CharField(max_length=18)
    street = forms.CharField(max_length=30)
    district = forms.CharField(max_length=20)
    city = forms.CharField(max_length=20)
    province = forms.CharField(max_length=20)
    rcategory = forms.CharField(max_length=20)