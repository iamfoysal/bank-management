from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import (users_list,
                    edit_user,
                    view_user,
                    delete_user,
                    create_user,
                    user_search,
                    user_login,
                    user_logout,
                    )

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('dashboard/users/', login_required(users_list), name='users_list'),
    path('dashboard/users/create/', login_required(create_user), name='create_user'),
    path('dashboard/users/<int:user_id>/', login_required(edit_user), name='edit_user'),
    path('dashboard/users/<int:user_id>/view/', login_required(view_user), name='view_user'),
    path('dashboard/users/<int:user_id>/delete/', login_required(delete_user), name='delete_user'),
    path('dashboard/search/', login_required(user_search), name='user_search'),

]
