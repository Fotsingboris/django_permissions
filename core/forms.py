from django import forms
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Blog, Product, Category

class UserPermissionForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.filter(
            codename__in=[
                'can_create_blog', 'can_update_blog', 'can_view_blog', 'can_delete_blog',
                'can_create_product', 'can_update_product', 'can_view_product', 'can_delete_product',
                'can_create_category', 'can_update_category', 'can_view_category', 'can_delete_category'
            ]
        ),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Permissions"
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput(),
        }
