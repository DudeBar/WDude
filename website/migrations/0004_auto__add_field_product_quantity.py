# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Product.quantity'
        db.add_column(u'website_product', 'quantity',
                      self.gf('django.db.models.fields.FloatField')(default=0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Product.quantity'
        db.delete_column(u'website_product', 'quantity')


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
        }
    }

    complete_apps = ['website']