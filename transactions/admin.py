from django.contrib import admin
from .models import BankAccount, Transaction


class BankAccountAdmin(admin.ModelAdmin):
    list_display = ["user", "account_number", "account_holder", "balance"]
    search_fields = ["user", "account_number", "account_holder"]
    list_filter = ["user", "account_number", "account_holder"]
    list_per_page = 10

    


class TransactionAdmin(admin.ModelAdmin):
    list_display = ["user", "transaction_id", "transaction_type", "receiver_name", "receiver_account", "transaction_amount", "transaction_status", ]
    search_fields = ["user", "transaction_id","receiver_name", "receiver_account", "transaction_amount", "transaction_status", "transaction_remarks"]
    list_per_page = 10



admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(Transaction, TransactionAdmin)


