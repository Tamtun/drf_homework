import django_filters
from users.models import Payment

class PaymentFilter(django_filters.FilterSet):
    ordering = django_filters.OrderingFilter(
        fields=(('date', 'date'),),
        field_labels={'date': 'Дата оплаты'},
        label='Сортировка'
    )

    class Meta:
        model = Payment
        fields = {
            'course': ['exact'],
            'lesson': ['exact'],
            'method': ['exact'],
        }
