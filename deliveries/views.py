from datetime import datetime

from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from deliveries.models import Delivery
from deliveries.serializers import DeliverySerializer


class DeliveryViewSet(viewsets.ModelViewSet):
    queryset = Delivery.objects.all()
    serializer_class = DeliverySerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["patch"], url_path="status")
    def update_status(self, request, pk=None):
        delivery = self.get_object()
        status_value = request.data.get("status")
        if status_value not in [choice[0] for choice in Delivery.STATUS_CHOICES]:
            return Response({"detail": "Invalid status"}, status=status.HTTP_400_BAD_REQUEST)
        delivery.status = status_value
        delivery.save()
        return Response(DeliverySerializer(delivery).data)

    @action(detail=False, methods=["get"], url_path="calendar")
    def calendar(self, request):
        customer_id = request.query_params.get("customer_id")
        month = request.query_params.get("month")
        if not customer_id or not month:
            return Response({"detail": "customer_id and month are required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            month_date = datetime.strptime(month, "%Y-%m")
        except ValueError:
            return Response({"detail": "Month must be in YYYY-MM format"}, status=status.HTTP_400_BAD_REQUEST)

        deliveries = Delivery.objects.filter(
            customer_id=customer_id,
            delivery_date__year=month_date.year,
            delivery_date__month=month_date.month,
        )
        return Response({
            "month": month,
            "days": [
                {
                    "date": item.delivery_date.isoformat(),
                    "status": item.status,
                }
                for item in deliveries
            ],
        })
