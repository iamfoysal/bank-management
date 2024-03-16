from django.shortcuts import render

# Create your views here.

# Path: accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404


def index(request):
    return render(request, 'index.html')
