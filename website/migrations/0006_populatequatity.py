# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import DataMigration
from django.db import models

class Migration(DataMigration):

    def forwards(self, orm):
        "Write your forwards methods here."
        # Note: Don't use "from appname.models import ModelName". 
        # Use orm.ModelName to refer to models in this application,
        # and orm['appname.ModelName'] for models in other applications.
        orm['website.ProductQuantity'].objects.create(type="demi", quantity=0.25)
        orm['website.ProductQuantity'].objects.create(type="pinte", quantity=0.5)
        orm['website.ProductQuantity'].objects.create(type="bouteille", quantity=0.33)

    def backwards(self, orm):
        "Write your backwards methods here."

    models = {
        u'website.billing': {
            'Meta': {'object_name': 'Billing'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'website.command': {
            'Meta': {'object_name': 'Command'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Customer']", 'null': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 11, 0, 0)'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total': ('django.db.models.fields.IntegerField', [], {})
        },
        u'website.customer': {
            'Meta': {'object_name': 'Customer'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'website.product': {
            'Meta': {'object_name': 'Product'},
            'command': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Command']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'price': ('django.db.models.fields.FloatField', [], {}),
            'product_id': ('django.db.models.fields.IntegerField', [], {}),
            'quantity': ('django.db.models.fields.FloatField', [], {'default': '0'})
        },
        u'website.productquantity': {
            'Meta': {'object_name': 'ProductQuantity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['website']
    symmetrical = True
