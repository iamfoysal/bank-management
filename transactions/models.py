from django.db import models
from users.models import CustomUser


class BankAccount(models.Model):
    name = models.CharField(max_length=100, null=True, verbose_name="bank Name")
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    

STATUS = (
    ("Success", "Success"),
    ("Failed", "Failed"),
)


TYPE= (
    ("Deposit", "Deposit"),
    ("Transfer", "Transfer"),
    ("Payment", "Payment"),
    ("Gift", "Gift"),
    ("Other", "Other"),
)






class Transaction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=20)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=20, choices=TYPE)
    receiver_name = models.CharField(max_length=100)
    receiver_account = models.CharField(max_length=20)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_status = models.CharField(max_length=20, choices=STATUS)
    transaction_remarks = models.CharField(max_length=100)

    def __str__(self):
        return self.user.first_name if self.user.first_name else self.transaction_id
    