from django.urls import path
from .views import SyncUserView,ProductViewSet
from rest_framework.routers import DefaultRouter

router=DefaultRouter()
router.register(r'products',ProductViewSet,basename="product")

urlpatterns = [
    path('auth/sync-user/',SyncUserView.as_view(),name="sync_user")
]

urlpatterns += router.urls