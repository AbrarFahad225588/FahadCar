from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Brand(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()
    image = models.ImageField(upload_to='cars/')

    def __str__(self):
        return self.name
    def buy(self, user):
        if self.quantity > 0:
            self.quantity -= 1
            self.save()
            PurchaseHistory.objects.create(user=user, car=self, purchase_date=timezone.now())

class PurchaseHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    purchase_date = models.DateTimeField()

    def __str__(self):
        return f"{self.user.username} bought {self.car.name} on {self.purchase_date}"
class Comment(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=255)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment