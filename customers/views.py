from django.db.models import Q
from rest_framework import filters, generics, permissions, status, viewsets
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from customers.import_service import import_customers
from customers.models import Customer
from customers.serializers import CustomerCreateSerializer, CustomerSerializer


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "create":
            return CustomerCreateSerializer
        return CustomerSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        phone = self.request.query_params.get("phone")
        if phone:
            qs = qs.filter(phone__icontains=phone)
        return qs


class CustomerSearchView(generics.ListAPIView):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ["phone", "name"]

    def get_queryset(self):
        phone = self.request.query_params.get("phone")
        if phone:
            return Customer.objects.filter(Q(phone__icontains=phone) | Q(name__icontains=phone))
        return Customer.objects.all()


class CustomerImportView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser]

    def post(self, request):
        upload = request.FILES.get("file") or request.FILES.get("csv")
        if not upload:
            return Response({"detail": "A CSV file is required in the file field."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(import_customers(upload), status=status.HTTP_200_OK)
