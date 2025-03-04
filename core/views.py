from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import transaction

from core.models import *
from .forms import *
from django.contrib.auth import  login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views import View


@login_required
def user_management(request):
    if request.method == 'POST':
        form = UserPermissionForm(request.POST)
        
        if form.is_valid():
            try:
                # Create the user without saving to DB yet
                user = form.save(commit=False)
                user.set_password(form.cleaned_data['password'])  # Set the password
                user.save()  # Save the user to the database
                
                # Assign selected permissions to the user
                permissions = form.cleaned_data.get('permissions', [])  # Default to empty list if no permissions are selected
                user.user_permissions.set(permissions)  # Assign permissions
                user.save()  # Save user again after assigning permissions
                
                messages.success(request, 'User Created Successfully')
                return redirect('dashboard')

            except Exception as e:
                # In case of any error, rollback and display error message
                messages.error(request, f"An error occurred while creating the user: {str(e)}")
                return redirect('user-management')
        else:
            # If form is invalid, show an error message
            print(request.POST)  # Debug: print submitted form data
            print(form.errors)  # Debug: print form errors to the console
            messages.error(request, 'Please correct the errors in the form.')
    else:
        form = UserPermissionForm()

    return redirect('all_users')


@login_required
def dashboard(request):
    # Define all available permissions (as button labels and their corresponding codename)
    available_permissions = [
        ('Create Blog', 'can_create_blog'),
        ('Update Blog', 'can_update_blog'),
        ('View Blog', 'can_view_blog'),
        ('Delete Blog', 'can_delete_blog'),
        ('Create Product', 'can_create_product'),
        ('Update Product', 'can_update_product'),
        ('View Product', 'can_view_product'),
        ('Delete Product', 'can_delete_product'),
        ('Create Category', 'can_create_category'),
        ('Update Category', 'can_update_category'),
        ('View Category', 'can_view_category'),
        ('Delete Category', 'can_delete_category')
    ]

    users_permissions = []

    # Check if the logged-in user is an admin
    if request.user.is_superuser:
        # Admin can see all users
        users = User.objects.all()
    else:
        # Regular users can only see their own permissions
        users = [request.user]  # Only their own user

    # For each user, check their permissions and create a list of accessible buttons
    for user in users:
        user_permissions = user.user_permissions.all().values_list('codename', flat=True)
        accessible_buttons = []

        # Check which buttons (permissions) the user has and add them to accessible_buttons
        for permission_label, permission_codename in available_permissions:
            if permission_codename in user_permissions:
                accessible_buttons.append(permission_label)

        users_permissions.append((user, accessible_buttons))  # Store user and accessible buttons

    return render(request, 'core/dashboard.html', {'users_permissions': users_permissions, 'available_permissions': available_permissions})


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


@login_required
def user_logout(request):
    # Log the user out
    logout(request)
    # Redirect to the login page or home page after logout
    return redirect('login')



def all_users(request):
    templates = 'core/users/users.html'
    
    # Define all available permissions (as button labels and their corresponding codename)
    available_permissions = [
        ('Create Blog', 'can_create_blog'),
        ('Update Blog', 'can_update_blog'),
        ('View Blog', 'can_view_blog'),
        ('Delete Blog', 'can_delete_blog'),
        ('Create Product', 'can_create_product'),
        ('Update Product', 'can_update_product'),
        ('View Product', 'can_view_product'),
        ('Delete Product', 'can_delete_product'),
        ('Create Category', 'can_create_category'),
        ('Update Category', 'can_update_category'),
        ('View Category', 'can_view_category'),
        ('Delete Category', 'can_delete_category')
    ]

    users_permissions = []

    # Check if the logged-in user is an admin
    if request.user.is_superuser:
        # Admin can see all users
        users = User.objects.all()
    else:
        # Regular users can only see their own permissions
        users = [request.user]  # Only their own user

    # For each user, check their permissions and create a list of accessible buttons
    for user in users:
        user_permissions = user.user_permissions.all().values_list('codename', flat=True)
        accessible_buttons = []

        # Check which buttons (permissions) the user has and add them to accessible_buttons
        for permission_label, permission_codename in available_permissions:
            if permission_codename in user_permissions:
                accessible_buttons.append(permission_label)

        users_permissions.append((user, accessible_buttons))  # Store user and accessible buttons
    
        form = UserPermissionForm()
    
    context = {
        'users_permissions': users_permissions, 
        'available_permissions': available_permissions,
        'form':form
    }
    return render(request, templates, context)


class CategoryView(PermissionRequiredMixin, View):
    permission_required = "core.can_view_category"

    def get(self, request):
        categories = Category.objects.all()
        form = CategoryForm()
        return render(request, "core/category/category_list.html", {"categories": categories, "form": form})

    def post(self, request):
        action = request.POST.get("action")

        # Permission checks for the actions
        if action == "create" and not request.user.has_perm('core.can_create_category'):
            messages.error(request, "You do not have permission to create a category.")
            return redirect("category")

        elif action == "update" and not request.user.has_perm('core.can_update_category'):
            messages.error(request, "You do not have permission to update a category.")
            return redirect("category")

        elif action == "delete" and not request.user.has_perm('core.can_delete_category'):
            messages.error(request, "You do not have permission to delete a category.")
            return redirect("category")

        try:
            with transaction.atomic():  # Begin transaction
                if action == "create":
                    form = CategoryForm(request.POST)
                    if form.is_valid():
                        form.save()
                        messages.success(request, "Category created successfully!")
                    else:
                        messages.error(request, "Error creating category.")

                elif action == "update":
                    category = get_object_or_404(Category, id=request.POST.get("category_id"))
                    form = CategoryForm(request.POST, instance=category)
                    if form.is_valid():
                        form.save()
                        messages.success(request, "Category updated successfully!")
                    else:
                        messages.error(request, "Error updating category.")

                elif action == "delete":
                    category = get_object_or_404(Category, id=request.POST.get("category_id"))
                    category.delete()
                    messages.success(request, "Category deleted successfully!")

        except Exception as e:
            # Rollback any changes if something goes wrong
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect("category")

    
class ProductView(PermissionRequiredMixin, View):
    permission_required = "core.can_view_product"

    def get(self, request):
        products = Product.objects.all()
        categories = Category.objects.all()
        form = ProductForm()
        return render(request, "core/product/product_list.html", {"products": products, "form": form, "categories": categories})

    def post(self, request):
        action = request.POST.get("action")

        # Check permissions for create, update, and delete actions
        if action == "create" and not request.user.has_perm('core.can_create_product'):
            messages.error(request, "You do not have permission to create a product.")
            return redirect("product")
        elif action == "update" and not request.user.has_perm('core.can_update_product'):
            messages.error(request, "You do not have permission to update a product.")
            return redirect("product")
        elif action == "delete" and not request.user.has_perm('core.can_delete_product'):
            messages.error(request, "You do not have permission to delete a product.")
            return redirect("product")

        try:
            with transaction.atomic():  # Begin transaction
                if action == "create":
                    form = ProductForm(request.POST, request.FILES)
                    if form.is_valid():
                        form.save()
                        messages.success(request, "Product created successfully!")
                    else:
                        print("Form errors:", form.errors)  # Debugging: Print errors
                        messages.error(request, "Form is not valid. Please check the input fields.")

                elif action == "update":
                    product = get_object_or_404(Product, id=request.POST.get("product_id"))
                    form = ProductForm(request.POST, request.FILES, instance=product)
                    if form.is_valid():
                        form.save()
                        messages.success(request, "Product updated successfully!")
                    else:
                        print("Form errors:", form.errors)  # Debugging: Print errors
                        messages.error(request, "Form is not valid. Please check the input fields.")

                elif action == "delete":
                    product = get_object_or_404(Product, id=request.POST.get("product_id"))
                    product.delete()
                    messages.success(request, "Product deleted successfully!")

        except Exception as e:
            # Rollback any changes if something goes wrong
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect("product")


class BlogView(PermissionRequiredMixin, View):
    permission_required = "core.can_view_blog"

    def get(self, request):
        blogs = Blog.objects.all()
        categories = Category.objects.all()
        form = BlogForm()
        return render(request, "core/blog/blog_list.html", {"blogs": blogs, "form": form, "categories": categories})

    def post(self, request):
        action = request.POST.get("action")

        # Check permissions for create, update, and delete actions
        if action == "create" and not request.user.has_perm('core.can_create_blog'):
            messages.error(request, "You do not have permission to create a blog.")
            return redirect("blog")
        elif action == "update" and not request.user.has_perm('core.can_update_blog'):
            messages.error(request, "You do not have permission to update a blog.")
            return redirect("blog")
        elif action == "delete" and not request.user.has_perm('core.can_delete_blog'):
            messages.error(request, "You do not have permission to delete a blog.")
            return redirect("blog")

        try:
            with transaction.atomic():  # Begin transaction
                if action == "create":
                    form = BlogForm(request.POST)
                    if form.is_valid():
                        form.save()
                        messages.success(request, "Blog created successfully!")
                    else:
                        print("Form errors:", form.errors)  # Debugging: Print errors
                        messages.error(request, "Form is not valid. Please check the input fields.")

                elif action == "update":
                    blog = get_object_or_404(Blog, id=request.POST.get("blog_id"))
                    form = BlogForm(request.POST, instance=blog)
                    if form.is_valid():
                        form.save()
                        messages.success(request, "Blog updated successfully!")
                    else:
                        print("Form errors:", form.errors)  # Debugging: Print errors
                        messages.error(request, "Form is not valid. Please check the input fields.")

                elif action == "delete":
                    blog = get_object_or_404(Blog, id=request.POST.get("blog_id"))
                    blog.delete()
                    messages.success(request, "Blog deleted successfully!")

        except Exception as e:
            # Rollback any changes if something goes wrong
            messages.error(request, f"An error occurred: {str(e)}")

        return redirect("blog")
