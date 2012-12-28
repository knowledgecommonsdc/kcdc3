# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Page'
        db.create_table('pinata_page', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('short_title', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('status', self.gf('django.db.models.fields.CharField')(default='CURRENT', max_length=9)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('path', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['pinata.Page'], null=True)),
            ('teaser', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('main_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('sidebar_text', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('pinata', ['Page'])


    def backwards(self, orm):
        # Deleting model 'Page'
        db.delete_table('pinata_page')


    models = {
        'pinata.page': {
            'Meta': {'ordering': "['path']", 'object_name': 'Page'},
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pinata.Page']", 'null': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'sidebar_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'CURRENT'", 'max_length': '9'}),
            'teaser': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['pinata']