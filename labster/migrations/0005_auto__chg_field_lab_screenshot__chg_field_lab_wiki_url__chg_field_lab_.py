# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Lab.screenshot'
        db.alter_column('labster_lab', 'screenshot', self.gf('django.db.models.fields.files.ImageField')(max_length=100))

        # Changing field 'Lab.wiki_url'
        db.alter_column('labster_lab', 'wiki_url', self.gf('django.db.models.fields.URLField')(max_length=120))

        # Changing field 'Lab.url'
        db.alter_column('labster_lab', 'url', self.gf('django.db.models.fields.URLField')(max_length=120))

    def backwards(self, orm):

        # Changing field 'Lab.screenshot'
        db.alter_column('labster_lab', 'screenshot', self.gf('django.db.models.fields.files.FileField')(max_length=100))

        # Changing field 'Lab.wiki_url'
        db.alter_column('labster_lab', 'wiki_url', self.gf('django.db.models.fields.CharField')(max_length=120))

        # Changing field 'Lab.url'
        db.alter_column('labster_lab', 'url', self.gf('django.db.models.fields.CharField')(max_length=120))

    models = {
        'labster.lab': {
            'Meta': {'object_name': 'Lab'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['labster.LanguageLab']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'questions': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'screenshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '120'}),
            'wiki_url': ('django.db.models.fields.URLField', [], {'max_length': '120', 'blank': 'True'})
        },
        'labster.languagelab': {
            'Meta': {'object_name': 'LanguageLab'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'language_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['labster']