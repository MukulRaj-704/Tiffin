from django.urls import path

from .views import BillDetailView, BillListView, GenerateBillView

urlpatterns = [
    path("generate/", GenerateBillView.as_view(), name="generate-bill"),
    path("customer/<int:customer_id>/", BillListView.as_view(), name="customer-bills"),
    path("<int:pk>/", BillDetailView.as_view(), name="bill-detail"),
]
