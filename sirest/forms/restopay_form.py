from django import forms

class restopay(forms.Form):
    nominal = forms.IntegerField(required=True)
