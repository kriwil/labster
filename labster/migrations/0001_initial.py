# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Token'
        db.create_table('labster_token', (
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('key', self.gf('django.db.models.fields.CharField')(max_length=40, primary_key=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('labster', ['Token'])

        # Adding model 'LanguageLab'
        db.create_table('labster_languagelab', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('language_code', self.gf('django.db.models.fields.CharField')(max_length=4)),
            ('language_name', self.gf('django.db.models.fields.CharField')(max_length=32)),
        ))
        db.send_create_signal('labster', ['LanguageLab'])

        # Adding model 'Lab'
        db.create_table('labster_lab', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('description', self.gf('django.db.models.fields.TextField')(default='')),
            ('url', self.gf('django.db.models.fields.URLField')(max_length=120)),
            ('wiki_url', self.gf('django.db.models.fields.URLField')(max_length=120, blank=True)),
            ('screenshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('questions', self.gf('django.db.models.fields.TextField')(default='', blank=True)),
            ('engine_xml', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('labster', ['Lab'])

        # Adding M2M table for field languages on 'Lab'
        db.create_table('labster_lab_languages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lab', models.ForeignKey(orm['labster.lab'], null=False)),
            ('languagelab', models.ForeignKey(orm['labster.languagelab'], null=False))
        ))
        db.create_unique('labster_lab_languages', ['lab_id', 'languagelab_id'])

        # Adding model 'CourseLab'
        db.create_table('labster_courselab', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lab', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labster.Lab'])),
            ('location', self.gf('django.db.models.fields.CharField')(unique=True, max_length=200)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('labster', ['CourseLab'])

        # Adding model 'LabProxy'
        db.create_table('labster_labproxy', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lab', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labster.Lab'])),
            ('location_id', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('labster', ['LabProxy'])

        # Adding unique constraint on 'LabProxy', fields ['lab', 'location_id']
        db.create_unique('labster_labproxy', ['lab_id', 'location_id'])

        # Adding model 'UserSave'
        db.create_table('labster_usersave', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lab_proxy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labster.LabProxy'])),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('save_file', self.gf('django.db.models.fields.files.FileField')(max_length=100, null=True, blank=True)),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('modified_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('labster', ['UserSave'])

        # Adding unique constraint on 'UserSave', fields ['lab_proxy', 'user']
        db.create_unique('labster_usersave', ['lab_proxy_id', 'user_id'])

        # Adding model 'ErrorInfo'
        db.create_table('labster_errorinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('lab_proxy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labster.LabProxy'])),
            ('browser', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('os', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('user_agent', self.gf('django.db.models.fields.CharField')(default='', max_length=200)),
            ('message', self.gf('django.db.models.fields.TextField')(default='')),
            ('date_encountered', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('labster', ['ErrorInfo'])

        # Adding model 'DeviceInfo'
        db.create_table('labster_deviceinfo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('lab_proxy', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labster.LabProxy'])),
            ('device_id', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('frame_rate', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('machine_type', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('os', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('ram', self.gf('django.db.models.fields.CharField')(default='', max_length=32)),
            ('processor', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('cores', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('gpu', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('memory', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('fill_rate', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('shader_level', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('date', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
            ('quality', self.gf('django.db.models.fields.CharField')(default='', max_length=128)),
            ('misc', self.gf('django.db.models.fields.TextField')(default='')),
            ('created_at', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now)),
        ))
        db.send_create_signal('labster', ['DeviceInfo'])


    def backwards(self, orm):
        # Removing unique constraint on 'UserSave', fields ['lab_proxy', 'user']
        db.delete_unique('labster_usersave', ['lab_proxy_id', 'user_id'])

        # Removing unique constraint on 'LabProxy', fields ['lab', 'location_id']
        db.delete_unique('labster_labproxy', ['lab_id', 'location_id'])

        # Deleting model 'Token'
        db.delete_table('labster_token')

        # Deleting model 'LanguageLab'
        db.delete_table('labster_languagelab')

        # Deleting model 'Lab'
        db.delete_table('labster_lab')

        # Removing M2M table for field languages on 'Lab'
        db.delete_table('labster_lab_languages')

        # Deleting model 'CourseLab'
        db.delete_table('labster_courselab')

        # Deleting model 'LabProxy'
        db.delete_table('labster_labproxy')

        # Deleting model 'UserSave'
        db.delete_table('labster_usersave')

        # Deleting model 'ErrorInfo'
        db.delete_table('labster_errorinfo')

        # Deleting model 'DeviceInfo'
        db.delete_table('labster_deviceinfo')


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
        'labster.courselab': {
            'Meta': {'object_name': 'CourseLab'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labster.Lab']"}),
            'location': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '200'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
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
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labster.Lab']"}),
            'location_id': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'})
        },
        'labster.languagelab': {
            'Meta': {'object_name': 'LanguageLab'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'language_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'labster.token': {
            'Meta': {'object_name': 'Token'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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