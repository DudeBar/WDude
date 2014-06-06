# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Product'
        db.create_table(u'website_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('product_id', self.gf('django.db.models.fields.IntegerField')()),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('price', self.gf('django.db.models.fields.FloatField')()),
            ('command', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['website.Command'])),
        ))
        db.send_create_signal(u'website', ['Product'])

        # Adding model 'Command'
        db.create_table(u'website_command', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 6, 6, 0, 0))),
            ('total', self.gf('django.db.models.fields.IntegerField')()),
            ('customer', self.gf('django.db.models.fields.IntegerField')(default=None, null=True)),
        ))
        db.send_create_signal(u'website', ['Command'])

        # Adding model 'Billing'
        db.create_table(u'website_billing', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('login', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=20)),
        ))
        db.send_create_signal(u'website', ['Billing'])


    def backwards(self, orm):
        # Deleting model 'Product'
        db.delete_table(u'website_product')

        # Deleting model 'Command'
        db.delete_table(u'website_command')

        # Deleting model 'Billing'
        db.delete_table(u'website_billing')


    models = {
        u'website.billing': {
            'Meta': {'object_name': 'Billing'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'login': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '20'})
        },
        u'website.command': {
            'Meta': {'object_name': 'Command'},
            'customer': ('django.db.models.fields.IntegerField', [], {'default': 'None', 'null': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 6, 6, 0, 0)'}),
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
            'product_id': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['website']