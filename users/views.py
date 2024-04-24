from decimal import Decimal
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views import View

from transactions.models import BankAccount, Transaction

from .models import CustomUser


def users_list(request):
    users = CustomUser.objects.filter(bank=request.user.bank, is_superuser=False)
    per_page = 10
    paginator = Paginator(users, per_page)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request, "users.html", {"users": page_obj})


def edit_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    if request.method == "POST":
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.save()
        messages.success(request, "User updated successfully")
        return redirect("edit_user", user_id=user.id)
    return render(request, "edit_user.html", {"user": user})


def view_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    return render(request, "view_user.html", {"user": user})


def delete_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.delete()
    messages.error(request, "User deleted successfully")
    return redirect("users_list")


def genaret_acount_number(previous_account_number):

    if previous_account_number == 0:
        return "00000000001"
    else:
        return str(int(previous_account_number) + 1).zfill(10)


def create_user(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        balance = request.POST.get("balance")
        last_user = CustomUser.objects.last()
        if last_user:
            last_account_number = last_user.account_number
        else:
            last_account_number = 0

        account_number = genaret_acount_number(last_account_number)
        get_user = CustomUser.objects.filter(email=email).first()

        if get_user:
            messages.error(request, "This email already used by another user")
            return redirect("create_user")
        customer = CustomUser.objects.create_user(
            email=email, first_name=first_name, last_name=last_name, account_number=account_number, password="password", bank=request.user.bank)
        if balance:
            bank = BankAccount.objects.get(pk=request.user.bank.id)
            if Decimal(balance) > request.user.bank.balance:
                messages.error(request, "Bank does not have enough balance")
                return redirect("create_user")
            customer.balance = balance
            customer.save()
            bank.balance -= Decimal(balance)
            bank.save()
        messages.success(request, "User created successfully")

        redirect("users_list")
    return render(request, "create_user.html")


def user_search(request):
    query = request.GET.get('q')
    bank = BankAccount.objects.get(pk=request.user.bank.id)

    if query:
        users = CustomUser.objects.filter(first_name__icontains=query) | CustomUser.objects.filter(
            last_name__icontains=query) | CustomUser.objects.filter(email__icontains=query).filter(bank__id=bank.id, is_superuser=False)
        transactions = (Transaction.objects.filter(user__first_name__icontains=query) | Transaction.objects.filter(
            user__last_name__icontains=query) | Transaction.objects.filter(user__email__icontains=query).filter(user__bank__id=bank.id))[:5]

    else:
        users = CustomUser.objects.filter(bank=request.user.bank)
    return render(request, 'search_user.html', {'users': users, 'query': query, 'transactions': transactions})


def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = None
        if "@" in username:
            user = authenticate(request, email=username, password=password)
        else:
            user = authenticate(request, username=username, password=password)

        if user and user.is_superuser:
            login(request, user)
            return redirect("dashboard")
        elif user and not user.is_superuser:
            login(request, user)
            return redirect("customer_dashboard")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("user_login")
    return render(request, "auth/login.html")


def user_logout(request):
    logout(request)
    messages.success(request, "You have been logged out")
    return redirect("user_login")



def create_customer(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        last_user = CustomUser.objects.last()
        if last_user:
            last_account_number = last_user.account_number
        else:
            last_account_number = 0

        account_number = genaret_acount_number(last_account_number)
        get_user = CustomUser.objects.filter(email=email).first()

        if get_user:
            messages.error(request, "This email already used by another user")
            return redirect("create_customer")
        else:
            customer = CustomUser.objects.create_user(email=email, first_name=first_name, last_name=last_name, account_number=account_number, password=password)
            bank = BankAccount.objects.filter(name="Northern").first()
            customer.bank = bank
            customer.balance = 0
            customer.save()

            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, "User created successfully")
                return redirect("customer_dashboard")
            else:
                messages.error(request, "Invalid credentials")
                return redirect("user_login")
      

    return render(request, "index.html")





def update_customer(request):
    if request.method == "POST":
        user = CustomUser.objects.get(id=request.user.id)
        user.first_name = request.POST.get("first_name")
        user.last_name = request.POST.get("last_name")
        user.email = request.POST.get("email")
        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect("update_customer")
    return render(request, "customer/edit_customer.html")




def view_customer(request):
    user = CustomUser.objects.get(id=request.user.id)
    return render(request, "view_customer.html", {"user": user})