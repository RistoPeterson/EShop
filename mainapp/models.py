from django.db import models

# Create your models here.

CATEGORY_CHOICES = (
	("F", "Garden"),
	("S", "Varia"),
	("M", "Home"),
	("T", "Car"),
	("R", "18+"),
)

class Item(models.Model):
	title = models.CharField(max_length=100)
	price = models.FloatField()
	discount_price = models.FloatField()
	category = models.CharField(choices=CATEGORY_CHOICES, max_length=5)
	slug = models.SlugField()
	description = models.TextField()
	image = models.ImageField()

	def __str__(self):
		return self.title