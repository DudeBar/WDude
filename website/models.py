import datetime
from django.db import models

class Customer(models.Model):
	login = models.CharField(max_length=20)
	password = models.CharField(max_length=20)

class Command(models.Model):
	date = models.DateTimeField(default=datetime.datetime.now())
	total = models.IntegerField()
	customer = models.IntegerField(null=True, default=None)

class Product(models.Model):
	product_id = models.IntegerField()
	name = models.CharField(max_length=50)
	price = models.FloatField()
	command = models.ForeignKey(Command)

class Billing(models.Model):
	login = models.CharField(max_length=20)
	password = models.CharField(max_length=20)