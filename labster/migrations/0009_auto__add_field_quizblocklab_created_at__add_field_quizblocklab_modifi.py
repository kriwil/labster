# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models
from django.utils import timezone


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'QuizBlockLab.created_at'
        db.add_column('labster_quizblocklab', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=timezone.now),
                      keep_default=False)

        # Adding field 'QuizBlockLab.modified_at'
        db.add_column('labster_quizblocklab', 'modified_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=timezone.now),
                      keep_default=False)

        # Adding field 'Lab.created_at'
        db.add_column('labster_lab', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=timezone.now),
                      keep_default=False)

        # Adding field 'Lab.modified_at'
        db.add_column('labster_lab', 'modified_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=timezone.now),
                      keep_default=False)

        # Adding field 'CourseProxy.created_at'
        db.add_column('labster_courseproxy', 'created_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=timezone.now),
                      keep_default=False)

        # Adding field 'CourseProxy.modified_at'
        db.add_column('labster_courseproxy', 'modified_at',
                      self.gf('django.db.models.fields.DateTimeField')(default=timezone.now),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'QuizBlockLab.created_at'
        db.delete_column('labster_quizblocklab', 'created_at')

        # Deleting field 'QuizBlockLab.modified_at'
        db.delete_column('labster_quizblocklab', 'modified_at')

        # Deleting field 'Lab.created_at'
        db.delete_column('labster_lab', 'created_at')

        # Deleting field 'Lab.modified_at'
        db.delete_column('labster_lab', 'modified_at')

        # Deleting field 'CourseProxy.created_at'
        db.delete_column('labster_courseproxy', 'created_at')

        # Deleting field 'CourseProxy.modified_at'
        db.delete_column('labster_courseproxy', 'modified_at')


    models = {
        'labster.courseproxy': {
            'Meta': {'object_name': 'CourseProxy'},
            'chapter_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'course_id': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'timezone.now'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labster.Lab']"}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'timezone.now'}),
            'position': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'section_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'unit_id': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'})
        },
        'labster.lab': {
            'Meta': {'object_name': 'Lab'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'timezone.now'}),
            'description': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['labster.LanguageLab']", 'symmetrical': 'False'}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'timezone.now'}),
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
            'Meta': {'ordering': "('lab__id', 'order')", 'object_name': 'QuizBlockLab'},
            'created_at': ('django.db.models.fields.DateTimeField', [], {'default': 'timezone.now'}),
            'description': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '120'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lab': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['labster.Lab']"}),
            'modified_at': ('django.db.models.fields.DateTimeField', [], {'default': 'timezone.now'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'questions': ('django.db.models.fields.TextField', [], {'default': "''"}),
            'quiz_block_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '64'})
        }
    }

    complete_apps = ['labster']