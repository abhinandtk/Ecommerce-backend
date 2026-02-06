from django.contrib import admin
from .models import User,Product,ProductVariant
from django.contrib.auth.admin import UserAdmin

# Register your models here.
@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model=User
    fieldsets = UserAdmin.fieldsets + (
        ( "Additional Info", {
            "fields" : ("dob" , "address" , "phone" ),
        } ),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Info", {
            "fields": ("dob", "address", "phone"),
        }),
    )

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "phone",
        "is_staff",
    )

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Basic Info", {
            "fields": ("name", "description"),
        }),
        ("Pricing & Inventory", {
            "fields": ("base_price",),
        }),
        ("Status", {
            "fields": ("is_active",),
        }),
    )

    list_display = ("name", "base_price", "is_active",)
    list_filter = ("is_active",)
    search_fields = ("name",)
    inlines=[ProductVariantInline]