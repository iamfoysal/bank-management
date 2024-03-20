
from .views import dashboard, transactions_list

from django.urls import path

urlpatterns = [
    path('dashboard/', dashboard, name='dashboard'),
    path('dashboard/transactions_list/', transactions_list, name='transactions-list'),
]