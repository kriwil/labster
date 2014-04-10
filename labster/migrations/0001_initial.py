# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
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
            ('objective', self.gf('django.db.models.fields.TextField')(default='')),
            ('engine_xml', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('url', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('wiki_url', self.gf('django.db.models.fields.CharField')(max_length=120)),
            ('screenshot', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal('labster', ['Lab'])

        # Adding M2M table for field languages on 'Lab'
        db.create_table('labster_lab_languages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('lab', models.ForeignKey(orm['labster.lab'], null=False)),
            ('languagelab', models.ForeignKey(orm['labster.languagelab'], null=False))
        ))
        db.create_unique('labster_lab_languages', ['lab_id', 'languagelab_id'])


    def backwards(self, orm):
        # Deleting model 'LanguageLab'
        db.delete_table('labster_languagelab')

        # Deleting model 'Lab'
        db.delete_table('labster_lab')

        # Removing M2M table for field languages on 'Lab'
        db.delete_table('labster_lab_languages')


    models = {
        'labster.lab': {
            'Meta': {'object_name': 'Lab'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'engine_xml': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['labster.LanguageLab']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'objective': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'screenshot': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '120'}),
            'wiki_url': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'labster.languagelab': {
            'Meta': {'object_name': 'LanguageLab'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'language_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['labster']