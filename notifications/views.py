from datetime import date

from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from deliveries.models import Delivery
from notifications.models import Notification
from notifications.serializers import NotificationSerializer


def requested_date(request):
    value = request.data.get("date") or request.query_params.get("date")
    if value:
        return date.fromisoformat(value)
    return date.today()


class ClockView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        try:
            clock_date = requested_date(request)
        except (TypeError, ValueError):
            return Response({"detail": "date must be in YYYY-MM-DD format"}, status=status.HTTP_400_BAD_REQUEST)

        created = []
        if clock_date.weekday() < 5:
            deliveries = Delivery.objects.filter(
                delivery_date=clock_date,
                subscription__start_date__lte=clock_date,
                subscription__end_date__gte=clock_date,
                subscription__status="ACTIVE",
                customer__isnull=False,
                status="SCHEDULED",
            ).exclude(
                subscription__pause_periods__start_date__lte=clock_date,
                subscription__pause_periods__end_date__gte=clock_date,
            ).select_related("customer")
            for delivery in deliveries:
                notification, was_created = Notification.objects.get_or_create(
                    delivery=delivery,
                    defaults={
                        "customer_id": delivery.customer_id,
                        "delivery_date": clock_date,
                        "message": "Your tiffin delivery is due today.",
                    },
                )
                if was_created:
                    created.append(notification)

        return Response(NotificationSerializer(created, many=True).data, status=status.HTTP_200_OK)


class OutboxView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        notifications = Notification.objects.all()
        delivery_date = request.query_params.get("date")
        if delivery_date:
            try:
                notifications = notifications.filter(delivery_date=date.fromisoformat(delivery_date))
            except ValueError:
                return Response({"detail": "date must be in YYYY-MM-DD format"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(NotificationSerializer(notifications, many=True).data)