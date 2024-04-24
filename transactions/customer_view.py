from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.serializers import serialize
from django.db.models import Sum
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.views import View

from users.models import CustomUser

from .models import BankAccount, Transaction


def customer_dashboard(request):
    request_user = request.user

    get_user = CustomUser.objects.get(id=request_user.id)
    if get_user.is_superuser==False:
        bank = get_user.bank
       
        total_transactions = Transaction.objects.filter(
            user=get_user).count()
        
        total_amount = Transaction.objects.filter(user=get_user, transaction_status="Success",).aggregate(
            Sum('transaction_amount'))['transaction_amount__sum']

        total_amount = total_amount if total_amount else 0
        list_ten__transactions = (Transaction.objects.filter(
            user=get_user).order_by('-transaction_date'))[:10]
        context = {
            "total_transactions": total_transactions,
            "transactions": list_ten__transactions,
            "balance": get_user.balance,
            "bank_name": bank.name,
            "total_amount": total_amount,
        }

        return render(request, "customer/customer_dashboard_home.html", context)
    else:
        messages.error(request, "You are not authorized to view this page")
        return redirect("index")


def customer_transactions_list(request):
    transactions = Transaction.objects.filter(user=request.user)
    per_page = 10
    paginator = Paginator(transactions, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "customer/transaction.html", {"transactions": page_obj})


def genaret_transaction_id(previous_transaction_id):

    if previous_transaction_id == 0:
        return "000000001"
    else:
        return str(int(previous_transaction_id) + 1).zfill(10)






def customer_transaction(request):
    users = CustomUser.objects.filter(
        bank=request.user.bank, is_superuser=False)
    
    if request.method == "POST":
        receiver_full_name = request.POST.get("receiver_name")
        amount = Decimal(request.POST.get("amount"))
        type = request.POST.get("transaction_type")
        transaction_remarks = request.POST.get("purpose")

        grt_user = CustomUser.objects.get(id=request.user.id)
        last_user = Transaction.objects.first()
        if last_user:
            last_account_number = last_user.transaction_id
        else:
            last_account_number = 0

        new_transaction_id = genaret_transaction_id(last_account_number)

        if type in ["Transfer", "Payment", "Gift"]:
            receiver = CustomUser.objects.filter(
                account_number=request.POST.get("receiver_account")).first()

            if receiver.account_number == grt_user.account_number:
                Transaction.objects.create(user=request.user,
                                           transaction_id=new_transaction_id,
                                           receiver_name=receiver_full_name if receiver_full_name else receiver.first_name,
                                           receiver_account=receiver.account_number,
                                           transaction_amount=amount,
                                           transaction_type=type,
                                           transaction_status="Failed",
                                           transaction_remarks=transaction_remarks)

                messages.error(request, "You cannot transfer to yourself")
                return redirect("customer_transfer")

            if not receiver:
                Transaction.objects.create(user=request.user,
                                           receiver_name=receiver_full_name if receiver_full_name else "Unknown",
                                           transaction_id=new_transaction_id,
                                           receiver_account=request.POST.get(
                                               "receiver_account"),
                                           transaction_amount=amount,
                                           transaction_type=type,
                                           transaction_status="Failed",
                                           transaction_remarks=transaction_remarks)
                messages.error(
                    request, "Failed! Invalid receiver account number")
                return redirect("customer_transfer")

            if request.user.balance >= amount:
                request.user.balance -= amount
                receiver.balance += amount
                if not receiver_full_name:
                    receiver_full_name = f"{receiver.first_name} {receiver.last_name}"
                request.user.save()
                receiver.save()
                Transaction.objects.create(user=request.user,
                                           receiver_name=receiver_full_name if receiver_full_name else receiver.first_name,
                                           transaction_id=new_transaction_id,
                                           receiver_account=receiver.account_number,
                                           transaction_amount=amount,
                                           transaction_type=type,
                                           transaction_status="Success",
                                           transaction_remarks=transaction_remarks)
                messages.success(request, "Transaction successful")
                return redirect("customer_transfer")
            else:
                messages.error(request, "Insufficient balance")
                return redirect("customer_transfer")
    context = {
        "users": users
    }
    return render(request, "customer/transfer.html", context)
