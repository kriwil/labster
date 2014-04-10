# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'Lab.engine_xml'
        db.delete_column('labster_lab', 'engine_xml')

        # Deleting field 'Lab.objective'
        db.delete_column('labster_lab', 'objective')


    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'Lab.engine_xml'
        raise RuntimeError("Cannot reverse this migration. 'Lab.engine_xml' and its values cannot be restored.")
        # Adding field 'Lab.objective'
        db.add_column('labster_lab', 'objective',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)


    models = {
        'labster.lab': {
            'Meta': {'object_name': 'Lab'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['labster.LanguageLab']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
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