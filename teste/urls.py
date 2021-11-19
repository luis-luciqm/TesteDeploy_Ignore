# urls.py
from django.urls import include, path

from . import views

urlpatterns = [
    # … other patterns
    path("select2/", include("django_select2.urls")),
    path("book/create", views.BookCreateView.as_view(), name="book-create"),
    path("adress/create", views.EnderecoCreateView.as_view(), name="book-create"),

]