import datetime
from django.db import models

TOTAL_BADE_LITRE = 5

class Customer(models.Model):
    login = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    bade = models.IntegerField(default=0)

    @property
    def quantity_litre(self):
        quantity = 0
        command_list = Command.objects.filter(customer=self)
        for command in command_list:
            for product in command.product_set.all():
                quantity += product.quantity.quantity
        return quantity

    @property
    def due_bade(self):
        total_conso = self.quantity_litre
        nb_bade = int(total_conso/TOTAL_BADE_LITRE)
        return nb_bade-self.bade

    def __unicode__(self):
        return self.login



class Command(models.Model):
    date = models.DateTimeField(default=datetime.datetime.now())
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