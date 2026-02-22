from rest_framework import serializers
from .models import Product,ProductVariant,Color,Size,Cart,CartItem


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Color
        fields="__all__"
class SizeSerailizer(serializers.ModelSerializer):
    class Meta:
        model=Size
        fields="__all__"
class ProductVariantSerializer(serializers.ModelSerializer):
    sizes=SizeSerailizer(read_only=True)
    colors=ColorSerializer(read_only=True)
    class Meta:
        model=ProductVariant
        fields="__all__"

class ProductSerializer(serializers.ModelSerializer):
    variants=ProductVariantSerializer(many=True,read_only=True)
    class Meta:
        model=Product
        fields="__all__"

class CartItemSerializer(serializers.ModelSerializer):
    product_variant = ProductVariantSerializer(read_only=True)
    product_name = serializers.CharField(source='product_variant.product.name', read_only=True)
    product_image = serializers.URLField(source='product_variant.product.image', read_only=True)
    
    class Meta:
        model = CartItem
        fields = ["id", "product_variant", "product_name", "product_image", "quantity"]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "status", "items", "total_price", "created_at", "updated_at"]

    def get_total_price(self, obj):
        return sum(item.product_variant.price * item.quantity for item in obj.items.all())
