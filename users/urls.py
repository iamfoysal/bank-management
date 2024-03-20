
from .views import users_list, edit_user, view_user, delete_user, create_user,user_search

from django.urls import path

urlpatterns = [
    path('dashboard/users/', users_list, name='users_list'),
    path('dashboard/users/create/', create_user, name='create_user'),
    path('dashboard/users/<int:user_id>/', edit_user, name='edit_user'),
    path('dashboard/users/<int:user_id>/view/', view_user, name='view_user'),
    path('dashboard/users/<int:user_id>/delete/', delete_user, name='delete_user'),
    path('search/', user_search, name='user_search'),
]