from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import ShippingAddressForm, CouponForm

from .models import Item, OrderItem, Order, BillingAddress, Coupon
from django.views.generic import View, DetailView, ListView


class IndexView(ListView):
    model = Item
    paginate_by = 8
    template_name = 'index.html'


class ProductDetailView(DetailView):
    model = Item
    template_name = 'product.html'


""" Add 1 item if clicked '+' icon """


@login_required
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


"""Remove 1 item if clicked '-' icon"""


@login_required
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


""" Trash icon function """


@login_required
def remove_from_cart(request, slug):
    order_item = OrderItem.objects.get(item__slug=slug, user=request.user, ordered=False)
    order_item.delete()
    return redirect('mainapp:summary')


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


class ShippingAddressView(View):
    def get(self, *args, **kwargs):
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            form = ShippingAddressForm()
            context = {
                'form': form,
                'order': order,
                'couponform': CouponForm(),
                'display_coupon_form': True,
            }
            return render(self.request, 'shipping_address.html', context)
        except ObjectDoesNotExist:
            messages.warning(self.request, 'You do not have an active order.')
            return redirect('mainapp:summary')

    def post(self, *args, **kwargs):
        form = ShippingAddressForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')

                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment=apartment_address,
                    country=country,
                    zip=zip_code,
                )

                billing_address.save()
                order.billing_address = billing_address
                order.save()

                messages.info(self.request, 'Address added to order.')
                return redirect('mainapp:summary')
        except ObjectDoesNotExist:
            messages.info(self.request, 'You do not have an active order.')
            return redirect('mainapp:summary')

def get_coupon(request, code):
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon is not valid")
        return redirect("mainapp:summary")


class addCouponView(View):
    def post(self, *args, **kwargs):
        form = CouponForm(self.request.POST or None)
        if form.is_valid():
            try:
                code = form.cleaned_data.get("code")
                order = Order.objects.get(user=self.request.user, ordered=False)
                order.coupon = get_coupon(self.request, code)
                order.save()
                messages.success(self.request, "Coupon added")
                return redirect("mainapp:shipping")
            except ObjectDoesNotExist:
                messages.info(self.request, "You do not have an active order")
                return redirect("mainapp:shipping")


def About(request):
    return render(request, "about.html")
