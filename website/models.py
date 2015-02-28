from datetime import datetime
from django.db import models
from django.db.models.aggregates import Sum

TOTAL_BADE_LITRE = 5


class Customer(models.Model):
    login = models.CharField(max_length=200)
    password = models.CharField(max_length=20)
    bade = models.IntegerField(default=0)

    @property
    def quantity_litre(self):
        quantity = Command.objects.filter(customer=self).aggregate(quantity=Sum('product__quantity__quantity'))
        return quantity['quantity'] or 0

    @property
    def quantity_day_litre(self):
        today = datetime.today()
        quantity = Command.objects.filter(customer=self, date__year=today.year, date__month=today.month,
                                          date__day=today.day).aggregate(quantity=Sum('product__quantity__quantity'))
        return quantity['quantity'] or 0

    @property
    def due_bade(self):
        total_conso = self.quantity_litre
        nb_bade = int(total_conso / TOTAL_BADE_LITRE)
        return nb_bade - self.bade

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
            return str(self.date) + " - " + self.customer.login + " : " + str(self.total)
        else:
            return str(self.date) + " : " + str(self.total)


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
    client_id = models.CharField(max_length=100)
    client_secret = models.CharField(max_length=100)


class WheelCustomer(models.Model):
    customer = models.ForeignKey(Customer, null=True)
    is_active = models.BooleanField(default=False)
    launch = models.BooleanField(default=False)

    def __unicode__(self):
        if self.is_active:
            return self.customer.login + " / c moi"
        else:
            return self.customer.login


class Commerces(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    tel = models.CharField(max_length=20, null=True, blank=True)
    contact = models.CharField(max_length=50, null=True, blank=True)
    type = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True, default=None)
    livraison = models.BooleanField(default=False)
    website = models.CharField(max_length=200, default=None, blank=True)
    ordre = models.IntegerField(default=0)
    image = models.CharField(max_length=200, default=None, blank=True)

    def __unicode__(self):
        return self.name


class MusicTrackAlreadyRegistered(Exception):
    pass


class MusicTrack(models.Model):
    artist = models.TextField(null=False)
    album = models.TextField(null=False)
    title = models.TextField(null=False)
    data = models.TextField(null=True)

    @classmethod
    def from_sonos_json(cls, data):
        track_data = {
            'album': data.get('album'),
            'title': data.get('title'),
            'artist': data.get('artist')
        }

        last_track = MusicTrack.objects.all().order_by('-pk').first()
        current_track = MusicTrack(**track_data)

        if last_track.artist == current_track.artist and last_track.album == current_track.album and last_track.title == current_track.title:
            raise MusicTrackAlreadyRegistered()

        return current_track
