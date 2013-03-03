# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Sponsor'
        db.create_table('pinata_sponsor', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('main_text', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('destination_url', self.gf('django.db.models.fields.URLField')(max_length=200, blank=True)),
            ('group', self.gf('django.db.models.fields.CharField')(default='B', max_length=3)),
            ('status', self.gf('django.db.models.fields.CharField')(default='CURRENT', max_length=9)),
            ('sort_order', self.gf('django.db.models.fields.IntegerField')(default=50, null=True, blank=True)),
        ))
        db.send_create_signal('pinata', ['Sponsor'])


    def backwards(self, orm):
        # Deleting model 'Sponsor'
        db.delete_table('pinata_sponsor')


    models = {
        'pinata.notice': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Notice'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'main_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'pinata.page': {
            'Meta': {'ordering': "['path']", 'object_name': 'Page'},
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'main_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['pinata.Page']", 'null': 'True', 'blank': 'True'}),
            'path': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'short_title': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'sidebar_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'CURRENT'", 'max_length': '9'}),
            'teaser': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'pinata.slide': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Slide'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'live': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'main_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        'pinata.sponsor': {
            'Meta': {'ordering': "['group', 'sort_order', 'title']", 'object_name': 'Sponsor'},
            'destination_url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'}),
            'group': ('django.db.models.fields.CharField', [], {'default': "'B'", 'max_length': '3'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'main_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'CURRENT'", 'max_length': '9'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        }
    }

    complete_apps = ['pinata']