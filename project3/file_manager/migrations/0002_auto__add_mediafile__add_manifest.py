# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'MediaFile'
        db.create_table(u'file_manager_mediafile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('manifest', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['file_manager.Manifest'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('version', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('release_date', self.gf('django.db.models.fields.DateField')()),
            ('content_type', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('language', self.gf('django.db.models.fields.CharField')(max_length=8)),
            ('barcode', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('md5_checksum', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal(u'file_manager', ['MediaFile'])

        # Adding model 'Manifest'
        db.create_table(u'file_manager_manifest', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('filename', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('all_media_present', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'file_manager', ['Manifest'])


    def backwards(self, orm):
        # Deleting model 'MediaFile'
        db.delete_table(u'file_manager_mediafile')

        # Deleting model 'Manifest'
        db.delete_table(u'file_manager_manifest')


    models = {
        u'file_manager.manifest': {
            'Meta': {'object_name': 'Manifest'},
            'all_media_present': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'file_manager.mediafile': {
            'Meta': {'object_name': 'MediaFile'},
            'barcode': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'content_type': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'filename': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'max_length': '8'}),
            'manifest': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['file_manager.Manifest']"}),
            'md5_checksum': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'release_date': ('django.db.models.fields.DateField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'version': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['file_manager']