
from .views import dashboard, transactions_list, index,transfer,transaction_grap_view
from .customer_view import customer_dashboard, customer_transactions_list,customer_transaction
from django.contrib.auth.decorators import login_required
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path("dashboard/transfer", login_required(transfer), name="transfer"),
    path('dashboard/', login_required(dashboard), name='dashboard'),
    path('dashboard/transactions_list/',
         login_required(transactions_list), name='transactions-list'),
        
    path('dashboard/transaction_graph/',
         login_required(transaction_grap_view), name='transaction-graph'),

    #  Customers 
    path('customer/dashboard/', login_required(customer_dashboard), name='customer_dashboard'),
    path('customer/transactions/',
         login_required(customer_transactions_list), name='customer_transactions_list'),
    path('customer/transfer', login_required(customer_transaction), name='customer_transfer'),
]
