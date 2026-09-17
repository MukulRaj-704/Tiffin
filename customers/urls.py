from django.urls import path

from .views import CustomerSearchView, CustomerViewSet

urlpatterns = [
    path("", CustomerViewSet.as_view({"get": "list", "post": "create"}), name="customer-list"),
    path("<int:pk>/", CustomerViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="customer-detail"),
    path("search/", CustomerSearchView.as_view(), name="customer-search"),
]
