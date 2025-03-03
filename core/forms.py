from django import forms
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType
from core.models import Blog, Product, Category

class UserPermissionForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.all(),
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Add specific permissions dynamically for each model
        blog_permissions = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Blog))
        product_permissions = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Product))
        category_permissions = Permission.objects.filter(content_type=ContentType.objects.get_for_model(Category))

        # Add permissions to the form fields
        self.fields['permissions'].queryset = blog_permissions | product_permissions | category_permissions
