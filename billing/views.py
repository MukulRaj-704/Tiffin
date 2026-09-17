from datetime import datetime

from django.db.models import Q
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from billing.models import Bill
from billing.serializers import BillSerializer
from customers.models import Customer
from subscriptions.models import Subscription


class GenerateBillView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        month = request.data.get("month")
        if not month:
            return Response({"detail": "month is required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            billing_month = datetime.strptime(month, "%Y-%m").date()
        except ValueError:
            return Response({"detail": "Month must be in YYYY-MM format"}, status=status.HTTP_400_BAD_REQUEST)

        customer_id = request.data.get("customer_id")
        if customer_id:
            subscriptions = Subscription.objects.filter(
                Q(customer_id=customer_id) | Q(deliveries__customer_id=customer_id)
            ).distinct()
        else:
            subscriptions = Subscription.objects.all()

        bills = []
        for subscription in subscriptions:
            bills.extend(BillSerializer(bill).data for bill in subscription.generate_monthly_bills(billing_month))

        return Response({"bills": bills}, status=status.HTTP_200_OK)


class BillListView(generics.ListAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        customer_id = self.kwargs.get("customer_id")
        if customer_id:
            return Bill.objects.filter(customer_id=customer_id)
        return Bill.objects.all()


class BillDetailView(generics.RetrieveAPIView):
    queryset = Bill.objects.all()
    serializer_class = BillSerializer
    permission_classes = [permissions.IsAuthenticated]
