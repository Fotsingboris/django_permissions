from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('user-management/', user_management, name='user_management'),
    path('dashboard/', dashboard, name='dashboard'),  # Create a simple dashboard view if needed
    path('users/', all_users, name='all_users'),  # Create a simple dashboard view if needed
        path('', login_view, name='login'),  # URL for the login page
        path('logout/', user_logout, name='logout'),
        
            path("category/", CategoryView.as_view(), name="category"),
            path("product/", ProductView.as_view(), name="product"),
    path("blog/", BlogView.as_view(), name="blog"),


]
