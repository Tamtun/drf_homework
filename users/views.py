from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from users.models import Payment
from users.serializers import PaymentSerializer
from users.filters import PaymentFilter

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = PaymentFilter
