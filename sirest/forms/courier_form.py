from django import forms

class CourierForm(forms.Form):
    email = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    name = forms.CharField(max_length=30)
    phonenum = forms.CharField(max_length=20)
    nik = forms.CharField(max_length=20)
    bankname = forms.CharField(max_length=20)
    accountno = forms.CharField(max_length=20)
    platenum = forms.CharField(max_length=10)
    drivinglicensenum = forms.CharField(max_length=20)
    vechicletype = forms.CharField(max_length=15)
    vehiclebrand = forms.CharField(max_length=15)