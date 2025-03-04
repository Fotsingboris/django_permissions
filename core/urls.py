from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('user-management/', user_management, name='user_management'),
    path('dashboard/', dashboard, name='dashboard'),  # Create a simple dashboard view if needed
        path('login/', login_view, name='login'),  # URL for the login page
        path('logout/', user_logout, name='logout'),

]
