# views.py
from django.views import generic

from . import forms, models



class BookCreateView(generic.CreateView):
    model = models.Book
    form_class = forms.BookForm
    success_url = "/"
    template_name='teste/book_form.html'

class EnderecoCreateView(generic.FormView):
    form_class = forms.AddressForm
    success_url = "/"
    template_name='teste/address_form.html'
