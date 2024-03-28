from django.contrib import admin
from .models import BankAccount, Transaction


class BankAccountAdmin(admin.ModelAdmin):
    list_display = ["name", "balance", "created_at", "updated_at",]


class TransactionAdmin(admin.ModelAdmin):
    list_display = ["user", "transaction_id", "transaction_type", "receiver_name",
                    "receiver_account", "transaction_amount", "transaction_status", "transaction_date"]
    search_fields = ["user", "transaction_id", "receiver_name", "receiver_account",
                     "transaction_amount", "transaction_status", "transaction_remarks"]
    list_per_page = 10


admin.site.register(BankAccount, BankAccountAdmin)
admin.site.register(Transaction, TransactionAdmin)
