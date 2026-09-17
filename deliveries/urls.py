from django.urls import path

from .views import DeliveryViewSet

urlpatterns = [
    path("", DeliveryViewSet.as_view({"get": "list", "post": "create"}), name="delivery-list"),
    path("<int:pk>/", DeliveryViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="delivery-detail"),
    path("<int:pk>/status/", DeliveryViewSet.as_view({"patch": "update_status"}), name="delivery-status"),
    path("calendar/", DeliveryViewSet.as_view({"get": "calendar"}), name="delivery-calendar"),
]
