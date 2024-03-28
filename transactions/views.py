from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.contrib import messages

from decimal import Decimal
from .models import BankAccount, Transaction
from users.models import CustomUser


def index(request):
    return render(request, 'index.html')


def dashboard(request):
    request_user = request.user

    get_user = CustomUser.objects.get(id=request_user.id)
    if get_user.is_superuser:
        bank = get_user.bank
        bank_balance = BankAccount.objects.get(pk=bank.id).balance
        total_transactions = Transaction.objects.filter(
            user__bank=bank.id).count()

        total_users = CustomUser.objects.filter(bank=bank).count()

        total_amount = Transaction.objects.filter(user__bank=bank, transaction_status="Success",).aggregate(
            Sum('transaction_amount'))['transaction_amount__sum']

        total_amount = total_amount if total_amount else 0
        last_tan_transactions = (Transaction.objects.filter(
            user__bank=bank).order_by('-transaction_date'))[:10]
        context = {
            "total_transactions": total_transactions,
            "total_users": total_users,
            "total_amount": total_amount,
            "transactions": last_tan_transactions,
            "bank_balance": bank_balance,
        }

        return render(request, "dashboard_home.html", context)
    else:
        messages.error(request, "You are not authorized to view this page")
        return redirect("index")


def transactions_list(request):
    transactions = Transaction.objects.filter(user__bank=request.user.bank)
    per_page = 10
    paginator = Paginator(transactions, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "transaction.html", {"transactions": page_obj})


def genaret_transaction_id(previous_transaction_id):

    if previous_transaction_id == 0:
        return "000000001"
    else:
        return str(int(previous_transaction_id) + 1).zfill(10)


def transfer(request):
    users = CustomUser.objects.filter(
        bank=request.user.bank, is_superuser=False)
    if request.method == "POST":
        sender = CustomUser.objects.get(id=request.POST.get("sender"))
        receiver_full_name = request.POST.get("receiver_name")
        amount = Decimal(request.POST.get("amount"))
        type = request.POST.get("transaction_type")
        transaction_remarks = request.POST.get("purpose")

        last_user = Transaction.objects.first()
        if last_user:
            last_account_number = last_user.transaction_id
        else:
            last_account_number = 0

        new_transaction_id = genaret_transaction_id(last_account_number)

        if type in ["Transfer", "Payment", "Gift"]:
            receiver = CustomUser.objects.filter(
                account_number=request.POST.get("receiver_account")).first()

            if request.POST.get("receiver") == sender.account_number:
                Transaction.objects.create(user=sender,
                                           transaction_id=new_transaction_id,
                                           receiver_name=receiver_full_name,
                                           receiver_account=receiver.account_number,
                                           transaction_amount=amount,
                                           transaction_type=type,
                                           transaction_status="Failed",
                                           transaction_remarks=transaction_remarks)

                messages.error(request, "You cannot transfer to yourself")
                return redirect("transfer")

            if not receiver:
                Transaction.objects.create(user=sender,
                                           receiver_name=receiver_full_name,
                                           transaction_id=new_transaction_id,
                                           receiver_account=request.POST.get(
                                               "receiver_account"),
                                           transaction_amount=amount,
                                           transaction_type=type,
                                           transaction_status="Failed",
                                           transaction_remarks=transaction_remarks)
                messages.error(
                    request, "Failed! Invalid receiver account number")
                return redirect("transfer")

            if sender.balance >= amount:
                sender.balance -= amount
                receiver.balance += amount
                if not receiver_full_name:
                    receiver_full_name = f"{receiver.first_name} {receiver.last_name}"
                sender.save()
                receiver.save()
                Transaction.objects.create(user=sender,
                                           receiver_name=receiver_full_name,
                                           transaction_id=new_transaction_id,
                                           receiver_account=receiver.account_number,
                                           transaction_amount=amount,
                                           transaction_type=type,
                                           transaction_status="Success",
                                           transaction_remarks=transaction_remarks)
                messages.success(request, "Transaction successful")
                return redirect("transfer")
            else:
                messages.error(request, "Insufficient balance")
                return redirect("transfer")

        elif type == "Deposit":
            bank = request.user.bank.id
            bank_account = BankAccount.objects.get(pk=bank)
            if bank_account.balance >= amount:
                bank_account.balance -= amount
                sender.balance += amount
                bank_account.save()
                sender.save()
                Transaction.objects.create(user=request.user,
                                           transaction_amount=amount,
                                           transaction_id=new_transaction_id,
                                           receiver_name=sender.first_name,
                                           receiver_account=sender.account_number,
                                           transaction_type=type,
                                           transaction_status="Success",
                                           transaction_remarks=transaction_remarks,)
                messages.success(request, "Deposit Transaction successful")
                return redirect("transfer")
            else:
                messages.error(request, "Insufficient balance")
                return redirect("transfer")
        elif type == "Withdrawal":
            bank = request.user.bank.id
            bank_account = BankAccount.objects.get(pk=bank)
            if sender.balance >= amount:
                bank_account.balance += amount
                sender.balance -= amount
                bank_account.save()
                sender.save()
                Transaction.objects.create(user=sender,
                                           transaction_amount=amount,
                                           transaction_id=new_transaction_id,
                                           receiver_account=sender.account_number,
                                           transaction_type=type,
                                           transaction_status="Success",
                                           transaction_remarks=transaction_remarks,)
                messages.success(request, "Withdraw Transaction successful")
                return redirect("transfer")
            else:
                messages.error(request, "Insufficient balance")
                return redirect("transfer")

    context = {
        "users": users
    }
    return render(request, "transactions/transfer.html", context)


from django.core.serializers import serialize
from django.http import JsonResponse


def transaction_grap_view(request):
    transactions_queryset = Transaction.objects.all()
    transactions_json = serialize('json', transactions_queryset)
    context = {
        'transactions_json': transactions_json
    }
    return render(request, 'transactions/map.html', context)