from django.urls import path

from notifications.views import ClockView, OutboxView

urlpatterns = [
    path("clock", ClockView.as_view(), name="clock"),
    path("outbox", OutboxView.as_view(), name="outbox"),
]