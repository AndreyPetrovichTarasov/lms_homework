import django_filters

from users.models import Payment


class PaymentFilter(django_filters.FilterSet):
    """
    Фильтры для модели Payment.
    """

    course = django_filters.CharFilter(
        field_name="course__name", lookup_expr="icontains"
    )
    lesson = django_filters.CharFilter(
        field_name="lesson__name", lookup_expr="icontains"
    )
    payment_method = django_filters.ChoiceFilter(
        field_name="payment_method",
        choices=Payment.PAYMENT_METHODS,
    )
    ordering = django_filters.OrderingFilter(
        fields=[
            ("date", "date"),
        ],
        field_labels={
            "date": "Дата оплаты",
        },
    )

    class Meta:
        model = Payment
        fields = ["course", "lesson", "payment_method"]
