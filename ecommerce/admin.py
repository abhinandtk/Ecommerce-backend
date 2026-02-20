from django.contrib import admin
from .models import User, Product, ProductVariant, Size, Color
from django.contrib.auth.admin import UserAdmin

# Register your models here.
admin.site.register(Size)
admin.site.register(Color)
admin.site.register(User)

# @admin.register(ProductVariant)
class ProductVariantAdmmin(admin.StackedInline):
    model=ProductVariant
    extra=1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines=[ProductVariantAdmmin]