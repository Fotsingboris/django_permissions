from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))

    class Meta:
        permissions = [
            ("can_create_category", _("Can Create Category")),
            ("can_update_category", _("Can Update Category")),
            ("can_view_category", _("Can View Category")),
            ("can_delete_category", _("Can Delete Category")),
        ]
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def __str__(self):
        return self.name


# Blog Model
class Blog(models.Model):
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    content = models.TextField(verbose_name=_("Content"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Category"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))

    class Meta:
        permissions = [
            ("can_create_blog", _("Can Create Blog")),
            ("can_update_blog", _("Can Update Blog")),
            ("can_view_blog", _("Can View Blog")),
            ("can_delete_blog", _("Can Delete Blog")),
        ]
        verbose_name = _("Blog")
        verbose_name_plural = _("Blogs")

    def __str__(self):
        return self.title


# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name=_("Name"))
    description = models.TextField(verbose_name=_("Description"))
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name=_("Category"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price"))

    class Meta:
        permissions = [
            ("can_create_product", _("Can Create Product")),
            ("can_update_product", _("Can Update Product")),
            ("can_view_product", _("Can View Product")),
            ("can_delete_product", _("Can Delete Product")),
        ]
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def __str__(self):
        return self.name
