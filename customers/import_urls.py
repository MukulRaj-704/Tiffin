from django.urls import path

from customers.views import CustomerImportView

urlpatterns = [
    path("", CustomerImportView.as_view(), name="customer-import"),
]