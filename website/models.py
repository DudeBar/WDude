import datetime
from django.db import models
from django.db.models.aggregates import Sum

TOTAL_BADE_LITRE = 5

class Customer(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    bade = models.IntegerField(default=0)

    @property
    def quantity_litre(self):
        quantity = Command.objects.filter(customer=self).aggregate(quantity=Sum('product__quantity__quantity'))
        return quantity['quantity'] or 0

    @property
    def due_bade(self):
        total_conso = self.quantity_litre
        nb_bade = int(total_conso/TOTAL_BADE_LITRE)
        return nb_bade-self.bade

    @property
    def nb_wheel(self):
        return WheelCustomer.objects.filter(customer=self).count()

    def __unicode__(self):
        return self.login



class Command(models.Model):
    date = models.DateTimeField(auto_now_add=True, blank=True)
    total = models.FloatField()
    customer = models.ForeignKey(Customer, null=True)

    def __unicode__(self):
        if self.customer:
            return str(self.date)+" - "+self.customer.login+" : "+str(self.total)
        else:
            return str(self.date)+" : "+str(self.total)

class ProductQuantity(models.Model):
    type = models.CharField(max_length=10)
    quantity = models.FloatField()

    def __unicode__(self):
        return self.type

class Product(models.Model):
    product_id = models.IntegerField()
    name = models.CharField(max_length=50)
    price = models.FloatField()
    quantity = models.ForeignKey(ProductQuantity)
    command = models.ForeignKey(Command)

    def __unicode__(self):
        return self.name

class Billing(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)

class FbAppAccount(models.Model):
    client_id=models.CharField(max_length=100)
    client_secret = models.CharField(max_length=100)

class WheelCustomer(models.Model):
    customer = models.ForeignKey(Customer, null=True)
    is_active = models.BooleanField(default=False)
    launch = models.BooleanField(default=False)
