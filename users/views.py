from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from django.views import View
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from transactions.models import Transaction


def users_list(request):
    users = CustomUser.objects.all()
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
        user.account_number = request.POST.get("account_number")
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
        CustomUser.objects.create_user(email=email, first_name=first_name, last_name=last_name,
                                       account_number=account_number, balance=balance, password="password")

        redirect("users_list")
    return render(request, "create_user.html")


def user_search(request):
    query = request.GET.get('q')
    if query:
        users = CustomUser.objects.filter(first_name__icontains=query) | CustomUser.objects.filter(
            last_name__icontains=query) | CustomUser.objects.filter(email__icontains=query)
        transactions = Transaction.objects.filter(user__first_name__icontains=query) | Transaction.objects.filter(
            user__last_name__icontains=query) | Transaction.objects.filter(user__email__icontains=query)

    else:
        users = CustomUser.objects.all()
    return render(request, 'search_user.html', {'users': users, 'query': query, 'transactions': transactions})
