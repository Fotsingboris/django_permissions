from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import UserPermissionForm

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

            return redirect('dashboard')
    else:
        form = UserPermissionForm()

    return render(request, 'core/user_management.html', {'form': form})
