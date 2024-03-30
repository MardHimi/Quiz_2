from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class User_profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    personal_id = models.CharField(max_length=11)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return self.user.email


class Account(models.Model):
    owner = models.ForeignKey(User_profile, on_delete=models.CASCADE)
    iBan = models.CharField(max_length=34)

    def __str__(self):
        return self.iBan


class card(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    exp_date = models.DateField()
    cvv = models.CharField(max_length=3)


class debt(models.Model):
    user = models.ForeignKey(User_profile, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def pay_debt(self, amount):
        self.amount -= amount
        self.save()