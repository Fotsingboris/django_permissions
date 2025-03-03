from django.urls import path
from .views import *

urlpatterns = [
    path('user-management/', user_management, name='user_management'),
    path('dashboard/', dashboard, name='dashboard'),  # Create a simple dashboard view if needed
]
