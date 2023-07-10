from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import ShippingAddressForm, CouponForm

from .models import Item, OrderItem, Order, BillingAddress, Coupon, Payment
from django.views.generic import View, DetailView, ListView

# import stripe
# import random
# import string
# from django.conf import settings

# stripe.api_key = settings.STRIPE_SECRET_KEY
""" reference order code """


# def create_order_code():
#     return "".join(random.choices(string.ascii_lowercase + string.digits, k=12))


class IndexView(ListView):
    model = Item
    paginate_by = 8
    template_name = 'all_products.html'


class ProductDetailView(DetailView):
    model = Item
    template_name = 'product.html'


@login_required
def add_to_cart(request, slug):
    item = get_object_or_404(Item, slug=slug)

    # Get or create the order item
    order_item, created = OrderItem.objects.get_or_create(
        item=item,
        user=request.user,
        ordered=False
    )

    # Check if there is an existing order for the user
    order_q = Order.objects.filter(user=request.user, ordered=False)

    if order_q.exists():
        # Retrieve the first order in the queryset
        order = order_q[0]

        if order.items.filter(item__slug=item.slug).exists():
            # If the item is already in the order, increase the quantity
            order_item.quantity += 1
            order_item.save()
            messages.info(request, "Item is successfully added to cart")
            return redirect("mainapp:summary")
        else:
            # If the item is not in the order, add it to the order
            messages.info(request, "Item is successfully added to cart")
            order.items.add(order_item)
            return redirect("mainapp:summary")
    else:
        # If there is no existing order, create a new order
        ordered_date = timezone.now()
        order = Order.objects.create(user=request.user, ordered_date=ordered_date)
        order.items.add(order_item)
        messages.info(request, "Item is successfully added to cart")
        return redirect("mainapp:summary")


@login_required
def remove_single_item(request, slug):
    item = get_object_or_404(Item, slug=slug)

    # Check if there is an existing order for the user
    order_q = Order.objects.filter(user=request.user, ordered=False)

    if order_q.exists():
        # Retrieve the first order in the queryset
        order = order_q[0]

        if order.items.filter(item__slug=item.slug).exists():
            # If the item is in the order, remove one quantity of the item
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
        # If there is no existing order, display a message
        messages.info(request, "You don't have an active order")
        return redirect("mainapp:detail", slug=slug)


@login_required
def remove_from_cart(request, slug):
    # "Trash icon function", to delete order item line.
    order_item = OrderItem.objects.get(item__slug=slug, user=request.user, ordered=False)
    order_item.delete()
    return redirect('mainapp:summary')


class OrderSummary(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        try:
            # Get the current active order for the user
            current_order = Order.objects.get(user=self.request.user, ordered=False)

            # Prepare the context data to be passed to the template
            context = {
                'object': current_order
            }

            # Render the summary.html template with the context
            return render(self.request, 'summary.html', context)

        except ObjectDoesNotExist:
            # If no active order exists, display a warning message and redirect
            messages.warning(self.request, "You don't have any items in the cart")
            return redirect('/')


class ShippingAddressView(View):
    def get(self, *args, **kwargs):
        try:
            # Get the current active order for the user
            order = Order.objects.get(user=self.request.user, ordered=False)

            # Initialize the shipping address form
            form = ShippingAddressForm()

            # Prepare the context data to be passed to the template
            context = {
                'form': form,
                'order': order,
                'couponform': CouponForm(),
                'display_coupon_form': True,
            }

            # Render the shipping_address.html template with the context
            return render(self.request, 'shipping_address.html', context)

        except ObjectDoesNotExist:
            # If no active order exists, display a warning message and redirect to the order summary page
            messages.warning(self.request, 'You do not have an active order.')
            return redirect('mainapp:summary')

    def post(self, *args, **kwargs):
        # Process the form submission for creating a billing address
        form = ShippingAddressForm(self.request.POST or None)

        try:
            # Get the current active order for the user
            order = Order.objects.get(user=self.request.user, ordered=False)

            if form.is_valid():
                # Extract the form data
                street_address = form.cleaned_data.get('street_address')
                apartment_address = form.cleaned_data.get('apartment_address')
                country = form.cleaned_data.get('country')
                zip_code = form.cleaned_data.get('zip_code')

                # Create a new billing address object
                billing_address = BillingAddress(
                    user=self.request.user,
                    street_address=street_address,
                    apartment=apartment_address,
                    country=country,
                    zip=zip_code,
                )

                billing_address.save()

                # Assign the billing address to the order
                order.billing_address = billing_address
                order.save()

                messages.info(self.request, 'Address added to order.')
                return redirect('mainapp:summary')

        except ObjectDoesNotExist:
            # If no active order exists, display a warning message and redirect to the order summary page
            messages.info(self.request, 'You do not have an active order.')
            return redirect('mainapp:summary')


def get_coupon(request, code):
    # Handles retrieving a coupon based on a provided code.
    try:
        coupon = Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request, "This coupon is not valid")
        return redirect("mainapp:summary")


class addCouponView(View):
    # Applies a coupon to an order and handles displaying messages and redirects based on the order's status.
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


class PaymentView(View):
    # Retrieves order, checks billing address, and renders payment or redirects to shipping.
    def get(self, *args, **kwargs):
        order = Order.objects.get(user=self.request.user, ordered=False)
        if order.billing_address:
            context = {
                'order': order,
                'display_coupon_form': False
            }
            return render(self.request, "payment.html", context)
        else:
            messages.warning(self.request, 'Please add your billing address')
            return redirect("mainapp:shipping")


""" Creditcard stripe functions """


# def post(self, *args, **kwargs):
#     order = Order.objects.get(user=self.request.user, ordered=False)
#     token = self.request.POST.get("stripeToken")
#     amount = int(order.total_price() * 100)
#
#     try:
#         charge = stripe.charge.create(
#            amount = amount,
#             currency = "eur",
#             source = token,
#             description = "Payment from Print3DStuff"
#         )
#         payment = Payment()
#         payment.stripe_charge_id = charge["id"]
#         payment.user = self.request.user
#         payment.amount = order.total_price()
#         payment.save()
#
#           """ If order success, cart template will show "0" """
#         order_items = order.items.all()
#         order_items.update(ordered=True)
#         for item in order_items:
#           item.payment = payment
#
#         order.order_ref = create_order_code()
#         order.save()
#
#         messages.success(self.request, "Order successful")
#         return redirect('/')
#
#     """ HERE COME COPY-PASTE FROM STRIPE INFO """


def About(request):
    return render(request, "about.html")


def HomeView(request):
    return render(request, "index.html")


@login_required
def Profile(request):
    username = request.user.username
    return render(request, "profile.html", {'username': username})
