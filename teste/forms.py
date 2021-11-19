# forms.py
from django import forms
from django_select2 import forms as s2forms

from .models import Book,Country,City
from django_select2.forms import Select2MultipleWidget
from django_select2.forms import ModelSelect2Widget


class AuthorWidget(s2forms.ModelSelect2Widget):
    search_fields = [
        "email__icontains",
    ]


class CoAuthorsWidget(s2forms.ModelSelect2MultipleWidget):
    search_fields = [
        "email__icontains",
    ]


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"
        widgets = {
            "author": AuthorWidget,
            "co_authors": CoAuthorsWidget,
        }

class AddressForm(forms.Form):
    country = forms.ModelChoiceField(queryset=Country.objects.all(),label=u"Country")

    city = forms.ModelChoiceField(
        queryset=City.objects.all(),
        label=u"City",
        
        widget=ModelSelect2Widget(
            model=City,
            search_fields=['name__icontains'],
            dependent_fields={'country': 'country'},
            max_results=500,
        )
        
    )