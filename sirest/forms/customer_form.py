from django import forms

class CustomerForm(forms.Form):
    email = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    name = forms.CharField(max_length=30)
    phonenum = forms.CharField(max_length=20)
    nik = forms.CharField(max_length=20)
    bankname = forms.CharField(max_length=20)
    accountno = forms.CharField(max_length=20)
    birthdate = forms.DateField()
    sex = forms.CharField(max_length=1)