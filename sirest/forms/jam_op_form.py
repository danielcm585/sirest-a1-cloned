from django import forms

class JamOpForms(forms.Form) :
    day = forms.CharField(max_length=10)
    starthours = forms.TimeField()
    endhours = forms.TimeField()