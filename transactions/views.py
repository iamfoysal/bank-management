from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum


from .models import BankAccount, Transaction
from users.models import CustomUser


def dashboard(request):
    total_transactions = Transaction.objects.count()
    total_users = CustomUser.objects.count()
    total_amount = Transaction.objects.aggregate(total_amount=Sum('transaction_amount'))['total_amount']
    total_amount = total_amount if total_amount else 0
    context = {
        "total_transactions": total_transactions,
        "total_users": total_users,
        "total_amount": total_amount
    }
    return render(request, "dashboard_home.html", context)


def transactions_list(request):
    # Get all transactions
    transactions = Transaction.objects.all()

    # Number of transactions per page
    per_page = 10

    # Create a paginator object
    paginator = Paginator(transactions, per_page)

    # Get the current page number from the request, default to 1
    page_number = request.GET.get('page', 1)

    # Get the transactions for the requested page
    page_obj = paginator.get_page(page_number)

    return render(request, "transaction.html", {"transactions": page_obj})



def create_transaction(request):
    if request.method == "POST":
        sender = request.user
        receiver = request.POST.get("receiver")
        amount = request.POST.get("amount")
        try:
            receiver = CustomUser.objects.get(account_number=receiver)
            amount = float(amount)
            if sender.balance >= amount:
                sender.balance -= amount
                receiver.balance += amount
                sender.save()
                receiver.save()
                Transaction.objects.create(sender=sender, receiver=receiver, transaction_amount=amount)
                return HttpResponse("Transaction successful")
            else:
                return HttpResponse("Insufficient balance")
        except CustomUser.DoesNotExist:
            return HttpResponse("Receiver not found")
    return render(request, "create_transaction.html")