# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'PublicSurvey'
        db.create_table('project_publicsurvey', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('survey_expiry_date', self.gf('django.db.models.fields.DateField')(null=True)),
            ('organization', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['accountmanagement.Organization'])),
            ('questionnaire_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('anonymous_web_submission_allowed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allowed_submission_count', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('anonymous_link_id', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('submissions_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('project', ['PublicSurvey'])

        # Adding unique constraint on 'PublicSurvey', fields ['organization', 'questionnaire_id']
        db.create_unique('project_publicsurvey', ['organization_id', 'questionnaire_id'])

        # Adding model 'ProjectGuest'
        db.create_table('project_projectguest', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('guest_name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('guest_email', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=0, max_length=1)),
            ('link_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=100)),
            ('public_survey', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['project.PublicSurvey'])),
        ))
        db.send_create_signal('project', ['ProjectGuest'])

        # Adding unique constraint on 'ProjectGuest', fields ['guest_email', 'public_survey']
        db.create_unique('project_projectguest', ['guest_email', 'public_survey_id'])


    def backwards(self, orm):
        
        # Removing unique constraint on 'ProjectGuest', fields ['guest_email', 'public_survey']
        db.delete_unique('project_projectguest', ['guest_email', 'public_survey_id'])

        # Removing unique constraint on 'PublicSurvey', fields ['organization', 'questionnaire_id']
        db.delete_unique('project_publicsurvey', ['organization_id', 'questionnaire_id'])

        # Deleting model 'PublicSurvey'
        db.delete_table('project_publicsurvey')

        # Deleting model 'ProjectGuest'
        db.delete_table('project_projectguest')


    models = {
        'accountmanagement.organization': {
            'Meta': {'object_name': 'Organization'},
            'account_type': ('django.db.models.fields.CharField', [], {'default': "'Pro SMS'", 'max_length': '20', 'null': 'True'}),
            'active_date': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'address': ('django.db.models.fields.TextField', [], {}),
            'addressline2': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'city': ('django.db.models.fields.TextField', [], {}),
            'country': ('django_countries.fields.CountryField', [], {'max_length': '2'}),
            'is_deactivate_email_sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'en'", 'max_length': '2', 'null': 'True'}),
            'name': ('django.db.models.fields.TextField', [], {}),
            'office_phone': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'org_id': ('django.db.models.fields.TextField', [], {'primary_key': 'True'}),
            'sector': ('django.db.models.fields.TextField', [], {}),
            'state': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'Activated'", 'max_length': '20', 'null': 'True'}),
            'status_changed_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'website': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'zipcode': ('django.db.models.fields.TextField', [], {})
        },
        'project.projectguest': {
            'Meta': {'unique_together': "(('guest_email', 'public_survey'),)", 'object_name': 'ProjectGuest'},
            'guest_email': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'guest_name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'public_survey': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['project.PublicSurvey']"}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0', 'max_length': '1'})
        },
        'project.publicsurvey': {
            'Meta': {'unique_together': "(('organization', 'questionnaire_id'),)", 'object_name': 'PublicSurvey'},
            'allowed_submission_count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'anonymous_link_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'anonymous_web_submission_allowed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accountmanagement.Organization']"}),
            'questionnaire_id': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'submissions_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'survey_expiry_date': ('django.db.models.fields.DateField', [], {'null': 'True'})
        },
        'project.reminder': {
            'Meta': {'object_name': 'Reminder'},
            'day': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'organization': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['accountmanagement.Organization']"}),
            'project_id': ('django.db.models.fields.CharField', [], {'max_length': '264'}),
            'reminder_mode': ('django.db.models.fields.CharField', [], {'default': "'before_deadline'", 'max_length': '20'})
        }
    }

    complete_apps = ['project']
