from django import forms

class FoodCategoryForm(forms.Form):
    name = forms.CharField(max_length=50)