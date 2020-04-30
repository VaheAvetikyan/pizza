from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Menu(models.Model):
    type = models.CharField(max_length=64)
    name = models.CharField(max_length=64)
    small = models.FloatField()
    large = models.FloatField()

    def __str__(self):
        return f"{self.type}: {self.name}: small - $ {self.small}, large - $ {self.large}"


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)

    small = "small"
    large = "large"
    SIZE_CHOICE = [(small, "small"),(large, "large")]
    size = models.CharField(max_length=5, choices=SIZE_CHOICE, default=small)

    def __str__(self):
        small = "small"
        return f"{self.user} - {self.item.name} ({self.item.type}): price - {self.size}"


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Menu, on_delete=models.CASCADE)

    price = models.FloatField(default=0)

    time = models.DateTimeField('date ordered')

    PENDING = "pending"
    DELIVERED = "delivered"
    STATUS_CHOICES = [(PENDING, "pending"), (DELIVERED, "delivered")]

    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"{self.user} __ {self.item.name} ({self.item.type}), price: $ {self.price}, ordered: {self.time} - status: {self.get_status_display()}"
