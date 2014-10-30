# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Commerces.ordre'
        db.add_column(u'website_commerces', 'ordre',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding field 'Commerces.image'
        db.add_column(u'website_commerces', 'image',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=200, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Commerces.ordre'
        db.delete_column(u'website_commerces', 'ordre')

        # Deleting field 'Commerces.image'
        db.delete_column(u'website_commerces', 'image')


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
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'total': ('django.db.models.fields.FloatField', [], {})
        },
        u'website.commerces': {
            'Meta': {'object_name': 'Commerces'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'contact': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'default': 'None', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'blank': 'True'}),
            'livraison': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'ordre': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tel': ('django.db.models.fields.CharField', [], {'max_length': '20', 'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'website': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '200', 'blank': 'True'})
        },
        u'website.customer': {
            'Meta': {'object_name': 'Customer'},
            'bade': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'website.fbappaccount': {
            'Meta': {'object_name': 'FbAppAccount'},
            'client_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'client_secret': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
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
        },
        u'website.wheelcustomer': {
            'Meta': {'object_name': 'WheelCustomer'},
            'customer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['website.Customer']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'launch': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['website']