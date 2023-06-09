from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .models import Item, OrderItem, Order
from django.views.generic import View, DetailView, ListView


class IndexView(ListView):
    model = Item
    paginate_by = 10
    template_name = 'index.html'


class ProductDetailView(DetailView):
    model = Item
    template_name = 'product.html'


@login_required(login_url='../accounts/login')
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )

    order_q = Order.objects.filter(user=request.user, ordered=False)

    if order_q.exists():
        order = order_q[0]

        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item is successfully added to cart")
            return redirect("mainapp:summary")
        else:
            messages.info(request, "Item is successfully added to cart")
            order.items.add(order_item)
            return redirect("mainapp:summary")

    else:
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item is successfully added to cart")
        return redirect("mainapp:summary")


@login_required(login_url='../accounts/login')
def remove_single_item(request, slug):
    item = get_object_or_404(Item, slug=slug)

    order_q = Order.objects.filter(user=request.user, ordered=False)

    if order_q.exists():
        order = order_q[0]

        if order.items.filter(item__slug=item.slug).exists():
            order_item = OrderItem.objects.filter(item=item, user=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order.items.remove(order_item)

            messages.info(request, "Item is removed from cart")
            return redirect("mainapp:summary")
        else:
            messages.info(request, "Item was not in your cart")
            return redirect("mainapp:detail", slug=slug)

    else:
        messages.info(request, "You dont have an active order")
        return redirect("mainapp:detail", slug=slug)


class OrderSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            current_order = Order.objects.get(user=self.request.user, ordered=False)
            context = {
                'object': current_order
            }
            return render(self.request, 'summary.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, "You don't have any item in the cart")
            return redirect('/')
        return render(self.request, 'summary.html')