# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Bio.web'
        db.add_column(u'classes_bio', 'web',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=255, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Bio.web'
        db.delete_column(u'classes_bio', 'web')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'classes.bio': {
            'Meta': {'ordering': "['name']", 'object_name': 'Bio'},
            'bio_email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'rating': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'role': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'role'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['classes.Role']"}),
            'show_email': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'staff_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'twitter': ('django.db.models.fields.CharField', [], {'max_length': '16', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'user'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['auth.User']"}),
            'web': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'classes.event': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Event'},
            'additional_dates_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'bio_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'details': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'documentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email_reminder': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'email_reminder_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email_welcome_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'end_time': ('django.db.models.fields.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'facilitators': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'facilitators'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'location'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['classes.Location']"}),
            'location_text': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'main_image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'max_students': ('django.db.models.fields.IntegerField', [], {'default': '999', 'null': 'True', 'blank': 'True'}),
            'partner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'partner'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['classes.Partner']"}),
            'registration_opens': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_status': ('django.db.models.fields.CharField', [], {'default': "'AUTO'", 'max_length': '7'}),
            'session': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'session'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': u"orm['classes.Session']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'PUBLISHED'", 'max_length': '9'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'students'", 'to': u"orm['auth.User']", 'through': u"orm['classes.Registration']", 'blank': 'True', 'symmetrical': 'False', 'null': 'True'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'teacher_bios': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'event'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['classes.Bio']"}),
            'teacher_text': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'teachers': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'teachers'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'thumbnail': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'type': ('django.db.models.fields.CharField', [], {'default': "'CLASS'", 'max_length': '9'}),
            'waitlist_status': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        u'classes.location': {
            'Meta': {'object_name': 'Location'},
            'address1': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'address2': ('django.db.models.fields.CharField', [], {'max_length': '60', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'default': "'Washington'", 'max_length': '60', 'blank': 'True'}),
            'hint': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'neighborhood': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'show_exact': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'state': ('django.db.models.fields.CharField', [], {'default': "'DC'", 'max_length': '2', 'blank': 'True'}),
            'zip': ('django.db.models.fields.CharField', [], {'max_length': '5', 'blank': 'True'})
        },
        u'classes.partner': {
            'Meta': {'object_name': 'Partner'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'blank': 'True'})
        },
        u'classes.registration': {
            'Meta': {'ordering': "['date_registered']", 'object_name': 'Registration'},
            'attended': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'cancelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'date_cancelled': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_promoted': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'date_registered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['classes.Event']", 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'late_promotion': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True'}),
            'waitlist': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'classes.role': {
            'Meta': {'ordering': "['sort_order']", 'object_name': 'Role'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'extended_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '48'}),
            'sort_order': ('django.db.models.fields.IntegerField', [], {'default': '50', 'null': 'True', 'blank': 'True'})
        },
        u'classes.session': {
            'Meta': {'ordering': "['slug']", 'object_name': 'Session'},
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'documentation': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'email_reminder_days': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'kicker': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'}),
            'long_title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'registration_status': ('django.db.models.fields.CharField', [], {'default': "'PREVENT'", 'max_length': '7'}),
            'show_sidebar_text': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'sidebar_text': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'CURRENT'", 'max_length': '9'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['classes']