from django.db import models
from product.models import Product, Category,Variation


# Create your models here.

class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.CharField(max_length=50)

    def __str__(self):
        return self.cart_id


class CartItems(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation,blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE) # foreignkey  Cart with cart_id
    quantity = models.IntegerField()


    def sub_total(self):
        return self.product.PRDPrice * self.quantity


    def __str__(self):
        return str(self.product)
