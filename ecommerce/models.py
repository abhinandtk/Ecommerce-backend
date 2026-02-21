from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    dob = models.DateField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=15, blank=True)

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.URLField(max_length=500, null=True, blank=True)
    badge = models.CharField(max_length=50, null=True, blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=50, unique=True)
    hex_value = models.CharField(max_length=7, null=True, blank=True)

    def __str__(self):
        return self.name
    
class ProductVariant(models.Model):
    product = models.ForeignKey(
        'Product',
        related_name="variants",
        on_delete=models.CASCADE
    )
    sizes = models.ForeignKey(Size,on_delete=models.SET_NULL, related_name="variants",null=True, blank=True)
    colors = models.ForeignKey(Color,on_delete=models.SET_NULL, related_name="variants",null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.product.name} Variant"