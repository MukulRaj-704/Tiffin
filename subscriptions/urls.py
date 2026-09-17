from django.urls import path

from .views import PausePeriodViewSet, SubscriptionViewSet

urlpatterns = [
    path("", SubscriptionViewSet.as_view({"get": "list", "post": "create"}), name="subscription-list"),
    path("<int:pk>/transfer/", SubscriptionViewSet.as_view({"post": "transfer"}), name="subscription-transfer"),
    path("<int:pk>/", SubscriptionViewSet.as_view({"get": "retrieve", "put": "update", "patch": "partial_update", "delete": "destroy"}), name="subscription-detail"),
    path("<int:pk>/pause/", SubscriptionViewSet.as_view({"post": "pause"}), name="subscription-pause"),
    path("<int:pk>/resume/", SubscriptionViewSet.as_view({"post": "resume"}), name="subscription-resume"),
    path("pause-periods/", PausePeriodViewSet.as_view({"get": "list"}), name="pause-period-list"),
]
