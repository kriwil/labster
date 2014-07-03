# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'DeviceInfo.labProxy'
        db.delete_column('labster_deviceinfo', 'labProxy_id')

        # Deleting field 'DeviceInfo.type'
        db.delete_column('labster_deviceinfo', 'type')

        # Adding field 'DeviceInfo.lab_proxy'
        db.add_column('labster_deviceinfo', 'lab_proxy',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['labster.LabProxy']),
                      keep_default=False)

        # Adding field 'DeviceInfo.machine_type'
        db.add_column('labster_deviceinfo', 'machine_type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'DeviceInfo.labProxy'
        db.add_column('labster_deviceinfo', 'labProxy',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=0, to=orm['labster.LabProxy']),
                      keep_default=False)

        # Adding field 'DeviceInfo.type'
        db.add_column('labster_deviceinfo', 'type',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=128),
                      keep_default=False)

        # Deleting field 'DeviceInfo.lab_proxy'
        db.delete_column('labster_deviceinfo', 'lab_proxy_id')

        # Deleting field 'DeviceInfo.machine_type'
        db.delete_column('labster_deviceinfo', 'machine_type')


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
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'labster.deviceinfo': {
            'Meta': {'object_name': 'DeviceInfo'},
            'cores': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'device_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'fill_rate': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'frame_rate': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'gpu': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab_proxy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labster.LabProxy']"}),
            'machine_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'memory': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'misc': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'os': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'processor': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'quality': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'ram': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'shader_level': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'labster.errorinfo': {
            'Meta': {'object_name': 'ErrorInfo'},
            'browser': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'date_encountered': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab_proxy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labster.LabProxy']"}),
            'message': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'os': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'user_agent': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200'})
        },
        'labster.lab': {
            'Meta': {'object_name': 'Lab'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'engine_xml': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['labster.LanguageLab']", 'symmetrical': 'False'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'questions': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'screenshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '120'}),
            'wiki_url': ('django.db.models.fields.URLField', [], {'max_length': '120', 'blank': 'True'})
        },
        'labster.labproxy': {
            'Meta': {'unique_together': "(('lab', 'location_id'),)", 'object_name': 'LabProxy'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labster.Lab']"}),
            'location_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'labster.languagelab': {
            'Meta': {'object_name': 'LanguageLab'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'language_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'labster.problem': {
            'Meta': {'object_name': 'Problem'},
            'answer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'content_markdown': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'content_xml': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'problem_type': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'quiz_block': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labster.QuizBlock']"})
        },
        'labster.quizblock': {
            'Meta': {'ordering': "('lab__name', 'order', 'created_at')", 'object_name': 'QuizBlock'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labster.Lab']"}),
            'lab_proxy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labster.LabProxy']", 'null': 'True', 'blank': 'True'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '200'})
        },
        'labster.quizblocklab': {
            'Meta': {'ordering': "('lab__id', 'order')", 'object_name': 'QuizBlockLab'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '120'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labster.Lab']"}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'questions': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'quiz_block_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        },
        'labster.token': {
            'Meta': {'object_name': 'Token'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'labster.userlabproxy': {
            'Meta': {'unique_together': "(('user', 'lab_proxy'),)", 'object_name': 'UserLabProxy'},
            'completed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab_proxy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labster.LabProxy']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'labster.userproblem': {
            'Meta': {'object_name': 'UserProblem'},
            'answer': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '200', 'blank': 'True'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_correct': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'problem': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labster.Problem']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        },
        'labster.usersave': {
            'Meta': {'unique_together': "(('lab_proxy', 'user'),)", 'object_name': 'UserSave'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab_proxy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labster.LabProxy']"}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'save_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['labster']