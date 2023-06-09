from django import template
from mainapp.models import Order

register = template.Library()


@register.filter(name="cart_count")
def cart_count(user):
    if user.is_authenticated:
        query_set = Order.objects.filter(user=user, ordered=False)
        if query_set.exists():
            return query_set[0].items.count()
        return 0
