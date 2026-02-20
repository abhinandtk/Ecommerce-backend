from django.urls import path
from .views import SyncUserView

urlpatterns = [
    path('auth/sync-user/',SyncUserView.as_view(),name="sync_user")
    
]
