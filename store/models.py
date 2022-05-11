from django.contrib.auth.models import User
from django.db import models


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=55)
    email = models.CharField(max_length=55)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=55)
    price = models.FloatField()
    digital = models.BooleanField(default=False, null=True, blank=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name

    @property
    def get_image_url(self):
        try:
            return self.image.url
        except:
            return ""


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=55, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_order_sum(self):
        items = self.orderitem_set.all()
        return sum([item.get_item_sum for item in items])

    @property
    def get_order_quantity(self):
        items = self.orderitem_set.all()
        return sum([item.quantity for item in items])

    @property
    def shipping(self):
        order_items = self.orderitem_set.all()
        for item in order_items:
            if not item.product.digital:
                return True
        return False


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_item_sum(self):
        return self.product.price * self.quantity


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order_id = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=55, null=True)
    city = models.CharField(max_length=55, null=True)
    district = models.CharField(max_length=55, null=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
