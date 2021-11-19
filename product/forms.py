from django.forms import ModelForm,Form
from django import forms

from .models import *
from management.models import Category, SubCategory, Store

from django_select2 import forms as s2forms

class ProductForm(ModelForm):
    price = forms.DecimalField(max_digits=8, decimal_places=2, localize=True)
    old_price = forms.DecimalField(max_digits=8, decimal_places=2, localize=True,required=False)
    subcategory = forms.ModelChoiceField(queryset= SubCategory.objects.all(), required=True)
    store = forms.ModelChoiceField(queryset=Store.objects.all(), required=True)
    freight = forms.ModelChoiceField(queryset=Freight.objects.all(), required=False)

    
    class Meta: 
        model= Product
        exclude  = ['user','relevant','created_at','slug']
        

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)

        # Header Image Field
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['warning'].widget.attrs['class'] = 'form-control selectric'
        self.fields['form_payment'].widget.attrs['class'] = 'form-control selectric'
        self.fields['freight'].widget.attrs['class'] = 'form-control selectric'
        self.fields['store'].widget.attrs['class'] = 'form-control selectric'
        self.fields['subcategory'].widget.attrs['class'] = 'form-control selectric'
        self.fields['long_url'].widget.attrs['class'] = 'form-control'
        self.fields['short_url'].widget.attrs['class'] = 'form-control'
        self.fields['status'].widget.attrs['class'] = 'form-control selectric'
        self.fields['coupon'].widget.attrs['class'] = 'form-control'
        self.fields['price'].widget.attrs['class'] = 'form-control'
        self.fields['price'].localize = True
        self.fields['price'].widget.is_localized = True
        self.fields['old_price'].widget.attrs['class'] = 'form-control'
        self.fields['old_price'].localize = True
        self.fields['old_price'].widget.is_localized = True

class CaptureForm(forms.Form):
    site_url =  forms.URLField()

class CategoriaWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "name__icontains",
    ]

class CategoriaForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {
            "category": CategoriaWidget,
        }
        
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        