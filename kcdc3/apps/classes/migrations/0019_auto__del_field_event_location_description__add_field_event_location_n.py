# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Event.location_description'
        db.delete_column('classes_event', 'location_description')

        # Adding field 'Event.location_neighborhood'
        db.add_column('classes_event', 'location_neighborhood',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Event.details'
        db.add_column('classes_event', 'details',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'Event.location_description'
        db.add_column('classes_event', 'location_description',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Deleting field 'Event.location_neighborhood'
        db.delete_column('classes_event', 'location_neighborhood')

        # Deleting field 'Event.details'
        db.delete_column('classes_event', 'details')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'classes.event': {
            'Meta': {'ordering': "['date']", 'object_name': 'Event'},
            'additional_dates_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'documentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email_reminder': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email_reminder_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email_welcome_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'facilitators': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'facilitators'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_address1': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'location_address2': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'location_city': ('django.db.models.fields.CharField', [], {'default': "'Washington'", 'max_length': '60', 'blank': 'True'}),
            'location_name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'location_neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'location_show_exact': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'location_state': ('django.db.models.fields.CharField', [], {'default': "'DC'", 'max_length': '2', 'blank': 'True'}),
            'location_zip': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'}),
            'main_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'max_students': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'registration_status': ('django.db.models.fields.CharField', [], {'default': "'AUTO'", 'max_length': '7'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PUBLISHED'", 'max_length': '9'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'students'", 'to': "orm['auth.User']", 'through': "orm['classes.Registration']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'teachers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'teachers'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'CLASS'", 'max_length': '9'}),
            'waitlist_status': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'classes.registration': {
            'Meta': {'ordering': "['date_registered']", 'object_name': 'Registration'},
            'attended': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_cancelled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_registered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['classes.Event']", 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True'}),
            'waitlist': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['classes']