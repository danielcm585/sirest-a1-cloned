from django import forms

class RestoCategoryForm(forms.Form):
    name = forms.CharField(max_length=50)

class IngredientForm(forms.Form):
    name = forms.CharField(max_length=50)