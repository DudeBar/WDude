from django.db import models

class Customer(models.Model):
	login = models.CharField(max_length=20)
	password = models.CharField(max_length=20)

