from django.db import models
from django.contrib.auth.models import User

# Category Model
class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        permissions = [
            ("can_create_category", "Can Create Category"),
            ("can_update_category", "Can Update Category"),
            ("can_view_category", "Can View Category"),
            ("can_delete_category", "Can Delete Category"),
        ]

    def __str__(self):
        return self.name


# Blog Model
class Blog(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        permissions = [
            ("can_create_blog", "Can Create Blog"),
            ("can_update_blog", "Can Update Blog"),
            ("can_view_blog", "Can View Blog"),
            ("can_delete_blog", "Can Delete Blog"),
        ]

    def __str__(self):
        return self.title


# Product Model
class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        permissions = [
            ("can_create_product", "Can Create Product"),
            ("can_update_product", "Can Update Product"),
            ("can_view_product", "Can View Product"),
            ("can_delete_product", "Can Delete Product"),
        ]

    def __str__(self):
        return self.name
