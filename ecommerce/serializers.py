from rest_framework import serializers
from .models import Product,ProductVariant,Color,Size


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