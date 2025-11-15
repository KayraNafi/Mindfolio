from django.urls import path
from . import views

urlpatterns = [
    # Global quotes page
    path('', views.quotes_list, name='quotes_list'),
]
