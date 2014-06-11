# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Renaming column for 'Product.quantity' to match new field type.
        db.rename_column(u'website_product', 'quantity', 'quantity_id')
        # Changing field 'Product.quantity'
        db.alter_column(u'website_product', 'quantity_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.ProductQuantity']))
        # Adding index on 'Product', fields ['quantity']
        db.create_index(u'website_product', ['quantity_id'])


    def backwards(self, orm):
        # Removing index on 'Product', fields ['quantity']
        db.delete_index(u'website_product', ['quantity_id'])


        # Renaming column for 'Product.quantity' to match new field type.
        db.rename_column(u'website_product', 'quantity_id', 'quantity')
        # Changing field 'Product.quantity'
        db.alter_column(u'website_product', 'quantity', self.gf('django.db.models.fields.FloatField')())

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
            'quantity': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.ProductQuantity']"})
        },
        u'website.productquantity': {
            'Meta': {'object_name': 'ProductQuantity'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quantity': ('django.db.models.fields.FloatField', [], {}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        }
    }

    complete_apps = ['website']