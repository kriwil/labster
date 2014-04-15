# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'QuizBlockLab'
        db.create_table('labster_quizblocklab', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('lab', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['labster.Lab'])),
            ('quiz_block_id', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('description', self.gf('django.db.models.fields.CharField')(default='', max_length=120)),
            ('questions', self.gf('django.db.models.fields.TextField')(default='')),
        ))
        db.send_create_signal('labster', ['QuizBlockLab'])


    def backwards(self, orm):
        # Deleting model 'QuizBlockLab'
        db.delete_table('labster_quizblocklab')


    models = {
        'labster.lab': {
            'Meta': {'object_name': 'Lab'},
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['labster.LanguageLab']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'questions': ('django.db.models.fields.TextField', [], {'default': "''", 'blank': 'True'}),
            'screenshot': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '120'}),
            'wiki_url': ('django.db.models.fields.URLField', [], {'max_length': '120', 'blank': 'True'})
        },
        'labster.languagelab': {
            'Meta': {'object_name': 'LanguageLab'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language_code': ('django.db.models.fields.CharField', [], {'max_length': '4'}),
            'language_name': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        },
        'labster.quizblocklab': {
            'Meta': {'object_name': 'QuizBlockLab'},
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '120'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labster.Lab']"}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'questions': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'quiz_block_id': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        }
    }

    complete_apps = ['labster']