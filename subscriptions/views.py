from datetime import date

from rest_framework import generics, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from deliveries.models import Delivery
from customers.models import Customer
from subscriptions.models import PausePeriod, Subscription
from subscriptions.serializers import PausePeriodSerializer, SubscriptionSerializer, SubscriptionTransferSerializer


class SubscriptionViewSet(viewsets.ModelViewSet):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"], url_path="pause")
    def pause(self, request, pk=None):
        subscription = self.get_object()
        start_date = request.data.get("start_date")
        end_date = request.data.get("end_date")
        reason = request.data.get("reason", "")
        try:
            pause = subscription.pause_subscription(start_date, end_date, reason)
            return Response(PausePeriodSerializer(pause).data, status=status.HTTP_200_OK)
        except Exception as exc:  # pragma: no cover
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], url_path="resume")
    def resume(self, request, pk=None):
        subscription = self.get_object()
        resume_date = request.data.get("resume_date")
        try:
            pause = subscription.resume_subscription(resume_date)
            return Response({"detail": "Subscription resumed successfully", "pause": PausePeriodSerializer(pause).data}, status=status.HTTP_200_OK)
        except Exception as exc:  # pragma: no cover
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"], url_path="transfer")
    def transfer(self, request, pk=None):
        subscription = self.get_object()
        new_customer_id = request.data.get("new_customer_id")
        transfer_date = request.data.get("transfer_date")
        try:
            new_customer = Customer.objects.get(pk=new_customer_id)
            parsed_date = date.fromisoformat(transfer_date)
            subscription.transfer(new_customer, parsed_date)
        except (Customer.DoesNotExist, TypeError, ValueError) as exc:
            return Response({"detail": str(exc) or "Invalid transfer request."}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as exc:  # pragma: no cover
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        transfer = subscription.transfers.latest("created_at")
        return Response(SubscriptionTransferSerializer(transfer).data, status=status.HTTP_200_OK)


class PausePeriodViewSet(viewsets.ModelViewSet):
    queryset = PausePeriod.objects.all()
    serializer_class = PausePeriodSerializer
    permission_classes = [permissions.IsAuthenticated]
