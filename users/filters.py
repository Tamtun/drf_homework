import django_filters
from lms.models import Payment

class PaymentFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields=(('created_at', 'created_at'),),
        field_labels={'created_at': 'Дата оплаты'},
        label='Сортировка'
    )

    class Meta:
        model = Payment
        fields = {
            'course': ['exact'],
        }
