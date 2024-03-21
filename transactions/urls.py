
from .views import dashboard, transactions_list
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    path('dashboard/', login_required(dashboard), name='dashboard'),
    path('dashboard/transactions_list/',
         login_required(transactions_list), name='transactions-list'),
]
