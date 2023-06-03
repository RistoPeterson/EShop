from django.contrib.auth.models import User
from django.db import models
from django.shortcuts import reverse
from django_countries.fields import CountryField


# Create your models here.

CATEGORY_CHOICES = (
    ("G", "Garden"),
    ("V", "Varia"),
    ("H", "Home"),
    ("C", "Car"),
    ("18", "18+"),
)


class Item(models.Model):
    title = models.CharField(max_length=100)
    price = models.FloatField()
    discount_price = models.FloatField(blank=True, null=True)
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
    slug = models.SlugField()
    description = models.TextField()
    image = models.ImageField()

    def __str__(self):
        return self.title

    def get_discount_percent(self):
        discount_percent = 100 - (self.discount_price * 100 / self.price)
        return discount_percent

    def get_item_url(self):
        return reverse('mainapp:product', kwargs={
            'slug': self.slug
        })


class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} - {self.item.title}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_ref = models.CharField(max_length=20)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField()
    ordered = models.BooleanField(default=False)
    billing_address = models.ForeignKey('BillingAddress', on_delete=models.SET_NULL, blank=True, null=True)
    coupon = models.ForeignKey('Coupon', on_delete=models.SET_NULL, blank=True, null=True)
    payment = models.ForeignKey('Payment', on_delete=models.SET_NULL, blank=True, null=True)
    delivered = models.BooleanField(default=False)
    received = models.BooleanField(default=False)
    refund_requested = models.BooleanField(default=False)
    refund_granted = models.BooleanField(default=False)

    def __str__(self):
        return self.user.name


class BillingAddress(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    street_name = models.CharField(max_length=100)
    country = CountryField(blank_label="(select country)", null=True)
    flat_number = models.CharField(max_length=5)
    zip = models.CharField(max_length=10)

    def __str__(self):
        return self.user.name


class Coupon(models.Model):
    code = models.CharField(max_length=100)
    amount = models.FloatField()

    def __str__(self):
        return self.code


class Payment(models.Model):
    stripe_charge_id = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.name


class Refund(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    reason = models.TextField
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.pk}"
