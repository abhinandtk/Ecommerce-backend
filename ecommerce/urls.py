from django.urls import path
from .views import SyncUserView,ProductViewSet,CartViewSet
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

router=DefaultRouter()
router.register(r'products',ProductViewSet,basename="product")
router.register(r'cart',CartViewSet,basename="cart")

urlpatterns = [
    path('auth/sync-user/',SyncUserView.as_view(),name="sync_user"),
    path("token/refresh/", TokenRefreshView.as_view()),
]

urlpatterns += router.urls