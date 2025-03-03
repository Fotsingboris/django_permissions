from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserPermissionForm
from django.contrib.auth import  login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages


@login_required
def user_management(request):
    if request.method == 'POST':
        form = UserPermissionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            
            # Assign permissions to the user
            permissions = form.cleaned_data['permissions']
            user.user_permissions.set(permissions)
            user.save()
            messages.success(request, 'User Created Successfully')
            

            return redirect('dashboard')
    else:
        
        form = UserPermissionForm()

    return render(request, 'core/user_management.html', {'form': form})


@login_required
def dashboard(request):
    # You can add more context here if needed, such as stats or data from your models
    return render(request, 'core/dashboard.html')


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, 'User Logged Successfully')
            
            return redirect('dashboard')  # Redirect to the dashboard after successful login
        else:
            messages.error(request, 'Invalid username or password')
    else:
        form = AuthenticationForm()
    
    return render(request, 'core/login.html', {'form': form})
