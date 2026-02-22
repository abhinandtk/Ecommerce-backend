from django.urls import path
from .views import SyncUserView,ProductViewSet,CartViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'products',ProductViewSet,basename="product")
router.register(r'cart',CartViewSet,basename="cart")

urlpatterns = [
    path('auth/sync-user/',SyncUserView.as_view(),name="sync_user")
]

urlpatterns += router.urls