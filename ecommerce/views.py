from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from rest_framework.viewsets import ModelViewSet,ViewSet
from .models import *
from .serializers import *
from django.db import transaction
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class SyncUserView(APIView):
    def post(self, request):
        try:
            email = request.data.get("email")
            if not email:
                return Response({"error": "Email is required"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Using email as username since it's required and should be unique
            user, created = User.objects.get_or_create(username=email, defaults={"email": email})
            
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            })
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ProductViewSet(ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer

from rest_framework.decorators import action

class CartViewSet(ViewSet):
    permission_classes=[IsAuthenticated]
    def list(self,request):
        cart,created=Cart.objects.get_or_create(
            user=request.user,
            status="ACTIVE"
        )
        serializer=CartSerializer(cart)
        return Response(serializer.data)
    @transaction.atomic
    def create(self, request):
        """
        POST /cart/
        Add product to cart
        """

        product_variant_id = request.data.get("product_variant")
        quantity = int(request.data.get("quantity", 1))

        if not product_variant_id:
            return Response(
                {"error": "product_variant is required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Get or create active cart
        cart, created = Cart.objects.get_or_create(
            user=request.user,
            status="ACTIVE"
        )

        # Check if item already exists
        cart_item, item_created = CartItem.objects.get_or_create(
            cart=cart,
            product_variant_id=product_variant_id,
            defaults={"quantity": quantity}
        )

        if not item_created:
            cart_item.quantity += quantity
            cart_item.save()

        serializer = CartSerializer(cart)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['patch'])
    def update_item(self, request):
        item_id = request.data.get("item_id")
        quantity = int(request.data.get("quantity", 1))
        
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user, cart__status="ACTIVE")
            if quantity > 0:
                item.quantity = quantity
                item.save()
            else:
                item.delete()
            
            cart = Cart.objects.get(user=request.user, status="ACTIVE")
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['delete'])
    def remove_item(self, request):
        item_id = request.data.get("item_id")
        try:
            item = CartItem.objects.get(id=item_id, cart__user=request.user, cart__status="ACTIVE")
            item.delete()
            
            cart = Cart.objects.get(user=request.user, status="ACTIVE")
            serializer = CartSerializer(cart)
            return Response(serializer.data)
        except CartItem.DoesNotExist:
            return Response({"error": "Item not found"}, status=status.HTTP_404_NOT_FOUND)