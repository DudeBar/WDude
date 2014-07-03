# coding=utf-8
from django.db import models
from website.models import Customer


class wheel_customer(models.Model):
    customer = models.ForeignKey(Customer, null=True)
    is_active = models.BooleanField(default=False)
    launch = models.BooleanField(default=False)