from django import forms
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Blog, Product, Category
from django.utils.translation import gettext_lazy as _

class UserPermissionForm(forms.ModelForm):
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        label="Confirm Password",
        required=True
    )

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
        fields = ['username', 'email', 'password', 'password2', 'permissions']  # Include all fields
        widgets = {
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'})
        }

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")

        if password1 and password2 and password1 != password2:
            self.add_error('password2', _('Passwords do not match.'))

        # Ensure permissions field is a list
        permissions = cleaned_data.get('permissions')
        if permissions is None:
            cleaned_data['permissions'] = []  # Default to empty list if no permissions are selected

        return cleaned_data