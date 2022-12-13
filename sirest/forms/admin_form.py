from django import forms

class AdminForm(forms.Form):
    email = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50)
    name = forms.CharField(max_length=30)
    phonenum = forms.CharField(max_length=20)