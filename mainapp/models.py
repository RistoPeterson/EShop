from django.db import models
from django.shortcuts import reverse

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


