# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Event.status'
        db.add_column('classes_event', 'status',
                      self.gf('django.db.models.fields.CharField')(default='PUBLISHED', max_length=9),
                      keep_default=False)

        # Adding field 'Event.featured'
        db.add_column('classes_event', 'featured',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Event.additional_dates_text'
        db.add_column('classes_event', 'additional_dates_text',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Event.location_name'
        db.add_column('classes_event', 'location_name',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=100, blank=True),
                      keep_default=False)

        # Adding field 'Event.location_address1'
        db.add_column('classes_event', 'location_address1',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=60, blank=True),
                      keep_default=False)

        # Adding field 'Event.location_address2'
        db.add_column('classes_event', 'location_address2',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=60, blank=True),
                      keep_default=False)

        # Adding field 'Event.location_city'
        db.add_column('classes_event', 'location_city',
                      self.gf('django.db.models.fields.TextField')(default='Washington', max_length=60, blank=True),
                      keep_default=False)

        # Adding field 'Event.location_state'
        db.add_column('classes_event', 'location_state',
                      self.gf('django.db.models.fields.TextField')(default='DC', max_length=2, blank=True),
                      keep_default=False)

        # Adding field 'Event.location_zip'
        db.add_column('classes_event', 'location_zip',
                      self.gf('django.db.models.fields.TextField')(default='', max_length=5, blank=True),
                      keep_default=False)

        # Adding field 'Event.location_show_exact'
        db.add_column('classes_event', 'location_show_exact',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Event.thumbnail'
        db.add_column('classes_event', 'thumbnail',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Event.main_image'
        db.add_column('classes_event', 'main_image',
                      self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Event.email_welcome_text'
        db.add_column('classes_event', 'email_welcome_text',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Event.email_reminder'
        db.add_column('classes_event', 'email_reminder',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)

        # Adding field 'Event.email_reminder_text'
        db.add_column('classes_event', 'email_reminder_text',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding field 'Event.documentation'
        db.add_column('classes_event', 'documentation',
                      self.gf('django.db.models.fields.TextField')(default='', blank=True),
                      keep_default=False)

        # Adding M2M table for field facilitators on 'Event'
        db.create_table('classes_event_facilitators', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('event', models.ForeignKey(orm['classes.event'], null=False)),
            ('user', models.ForeignKey(orm['auth.user'], null=False))
        ))
        db.create_unique('classes_event_facilitators', ['event_id', 'user_id'])


        # Changing field 'Event.location_description'
        db.alter_column('classes_event', 'location_description', self.gf('django.db.models.fields.TextField')())

    def backwards(self, orm):
        # Deleting field 'Event.status'
        db.delete_column('classes_event', 'status')

        # Deleting field 'Event.featured'
        db.delete_column('classes_event', 'featured')

        # Deleting field 'Event.additional_dates_text'
        db.delete_column('classes_event', 'additional_dates_text')

        # Deleting field 'Event.location_name'
        db.delete_column('classes_event', 'location_name')

        # Deleting field 'Event.location_address1'
        db.delete_column('classes_event', 'location_address1')

        # Deleting field 'Event.location_address2'
        db.delete_column('classes_event', 'location_address2')

        # Deleting field 'Event.location_city'
        db.delete_column('classes_event', 'location_city')

        # Deleting field 'Event.location_state'
        db.delete_column('classes_event', 'location_state')

        # Deleting field 'Event.location_zip'
        db.delete_column('classes_event', 'location_zip')

        # Deleting field 'Event.location_show_exact'
        db.delete_column('classes_event', 'location_show_exact')

        # Deleting field 'Event.thumbnail'
        db.delete_column('classes_event', 'thumbnail')

        # Deleting field 'Event.main_image'
        db.delete_column('classes_event', 'main_image')

        # Deleting field 'Event.email_welcome_text'
        db.delete_column('classes_event', 'email_welcome_text')

        # Deleting field 'Event.email_reminder'
        db.delete_column('classes_event', 'email_reminder')

        # Deleting field 'Event.email_reminder_text'
        db.delete_column('classes_event', 'email_reminder_text')

        # Deleting field 'Event.documentation'
        db.delete_column('classes_event', 'documentation')

        # Removing M2M table for field facilitators on 'Event'
        db.delete_table('classes_event_facilitators')


        # Changing field 'Event.location_description'
        db.alter_column('classes_event', 'location_description', self.gf('django.db.models.fields.TextField')(max_length=200))

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
            'documentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email_reminder': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email_reminder_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email_welcome_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'facilitators': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'facilitators'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location_address1': ('django.db.models.fields.TextField', [], {'max_length': '60', 'blank': 'True'}),
            'location_address2': ('django.db.models.fields.TextField', [], {'max_length': '60', 'blank': 'True'}),
            'location_city': ('django.db.models.fields.TextField', [], {'default': "'Washington'", 'max_length': '60', 'blank': 'True'}),
            'location_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'location_name': ('django.db.models.fields.TextField', [], {'max_length': '100', 'blank': 'True'}),
            'location_show_exact': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'location_state': ('django.db.models.fields.TextField', [], {'default': "'DC'", 'max_length': '2', 'blank': 'True'}),
            'location_zip': ('django.db.models.fields.TextField', [], {'max_length': '5', 'blank': 'True'}),
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