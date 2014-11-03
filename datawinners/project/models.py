# vim: ai ts=4 sts=4 et sw= encoding=utf-8
from datetime import timedelta, date

from couchdb.mapping import TextField
from django.db.models import CASCADE
from django.db.models.fields import IntegerField, CharField
from django.db.models.fields.related import ForeignKey
from django.db import models, IntegrityError

from datawinners.accountmanagement.models import Organization
from datawinners.project.couch_view_helper import get_all_projects
from mangrove.datastore.database import DatabaseManager, DataObject
from mangrove.datastore.documents import DocumentBase, TZAwareDateTimeField, ProjectDocument
from mangrove.form_model.project import Project
from mangrove.utils.types import is_string, is_empty

NUMBER_OF_NONPROJECT_FORMMODELS = 2 #DS registration and delete form models
def get_all_reminder_logs_for_project(project_id, dbm):
    assert isinstance(dbm, DatabaseManager)
    rows = dbm.view.reminder_log(startkey=project_id, endkey=project_id, include_docs=True)
    return [ReminderLog.new_from_doc(dbm=dbm, doc=ReminderLog.__document_class__.wrap(row['doc'])) for row in rows]


class ReminderRepository(object):
    def get_all_reminders_for(self, organization_id):
        return Reminder.objects.filter(organization=organization_id)


def get_reminder_repository():
    return ReminderRepository()


class ReminderMode(object):
    BEFORE_DEADLINE = 'before_deadline'
    ON_DEADLINE = 'on_deadline'
    AFTER_DEADLINE = 'after_deadline'


class RemindTo(object):
    ALL_DATASENDERS = 'all_datasenders'
    DATASENDERS_WITHOUT_SUBMISSIONS = 'datasenders_without_submissions'


class Reminder(models.Model):
    project_id = CharField(null=False, blank=False, max_length=264)
    day = IntegerField(null=True, blank=True)
    message = CharField(max_length=160)
    reminder_mode = CharField(null=False, blank=False, max_length=20, default=ReminderMode.BEFORE_DEADLINE)
    organization = ForeignKey(Organization)

    def to_dict(self):
        return {'day': self.day, 'message': self.message, 'reminder_mode': self.reminder_mode, 'id': self.id}

    def void(self, void=True):
        self.voided = void
        self.save()

    def should_be_send_on(self, deadline, on_date):
        assert isinstance(on_date, date)
        deadline_date = self._get_applicapable_deadline_date(deadline, on_date)
        return on_date == deadline_date + timedelta(days=self._delta())

    def get_sender_list(self, project, on_date, dbm):
        if not project.reminder_and_deadline['should_send_reminder_to_all_ds']:
            deadline_date = self._get_applicapable_deadline_date(project.deadline(), on_date)
            return project.get_data_senders_without_submissions_for(deadline_date, dbm, project._frequency_period())
        return project.get_data_senders(dbm)

    def _delta(self):
        if self.reminder_mode == ReminderMode.ON_DEADLINE:
            return 0
        if self.reminder_mode == ReminderMode.BEFORE_DEADLINE:
            return -self.day
        if self.reminder_mode == ReminderMode.AFTER_DEADLINE:
            return self.day

    def _get_applicapable_deadline_date(self, deadline, on_date):
        if self.reminder_mode == ReminderMode.BEFORE_DEADLINE:
            return deadline.next_deadline(on_date)
        else:
            return deadline.current_deadline(on_date)

    def log(self, dbm, project_id, date, to_number, sent_status='sent', number_of_sms=0):
        log = ReminderLog(dbm=dbm, reminder=self, project_id=project_id, date=date, sent_status=sent_status,
                          number_of_sms=number_of_sms, to_number=to_number)
        log.save()
        return log

class PublicSurvey(models.Model):
    survey_expiry_date = models.DateField(null=True)
    organization = models.ForeignKey('accountmanagement.Organization', on_delete=CASCADE, null=False)
    questionnaire_id = models.CharField(max_length=100)
    anonymous_web_submission_allowed = models.BooleanField(default=False)
    allowed_submission_count = models.IntegerField(null=True) # max 2147483647
    anonymous_link_id = models.CharField(max_length=100)
    submissions_count = models.IntegerField(default=0)

    class Meta:
        # to support custom link
        unique_together = ('organization', 'questionnaire_id')

    def mark_submission_taken(self):
        self.submissions_count += 1
        self.save()

def create_public_survey(org_id, questionnaire_id):
    from datawinners.project.public_project_guest_handler import UniqueIdGenerator
    project_survey = PublicSurvey.objects.create(organization=Organization.objects.get(org_id=org_id),
                                                 questionnaire_id=questionnaire_id,
                                                 anonymous_link_id=UniqueIdGenerator().get_unique_id())
    return project_survey


def get_or_create_public_survey_of(questionnaire_id, org_id):
    public_surveys = PublicSurvey.objects.filter(organization=org_id).filter(questionnaire_id=questionnaire_id)
    if len(public_surveys) > 0:
        public_survey = public_surveys[0]
    else:
        try:
            public_survey = create_public_survey(org_id, questionnaire_id)
        except IntegrityError:
            # retry once
            public_survey = create_public_survey(org_id, questionnaire_id)


    return public_survey


class ProjectGuest(models.Model):
    EMAIL_TO_BE_SEND = 0
    EMAIL_SEND = 1
    SURVEY_TAKEN = 2
    STATUS_CHOICES = (
        (EMAIL_TO_BE_SEND, 'Email to be sent'),
        (EMAIL_SEND, 'Email send'),
        (SURVEY_TAKEN, 'Survey taken')
    )

    guest_name = models.CharField(max_length=100)
    guest_email = models.CharField(max_length=100)
    status = models.IntegerField(choices=STATUS_CHOICES, max_length=1, default=EMAIL_TO_BE_SEND)
    link_id = models.CharField(max_length=100, unique=True)
    public_survey = models.ForeignKey(PublicSurvey, null=False, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('guest_email', 'public_survey')

    def mark_email_send(self):
        self.status = self.EMAIL_SEND
        self.save()

    def mark_submission_taken(self):
        self.status = self.SURVEY_TAKEN
        self.save()

    def get_status_label(self):
        return [v for t,v in ProjectGuest.STATUS_CHOICES if self.status == t][0]

class ReminderLogDocument(DocumentBase):
    reminder_id = TextField()
    project_id = TextField()
    sent_status = TextField()
    number_of_sms = TextField()
    date = TZAwareDateTimeField()
    message = TextField()
    remind_to = TextField()
    reminder_mode = TextField()

    def __init__(self, id=None, reminder_id=None, project_id=None, sent_status=None, number_of_sms=None, date=None,
                 message=None, remind_to=None, reminder_mode=None):
        DocumentBase.__init__(self, id=id, document_type='ReminderLog')
        self.reminder_id = reminder_id
        self.project_id = project_id
        self.sent_status = sent_status
        self.number_of_sms = number_of_sms
        self.date = date
        self.message = message
        self.remind_to = remind_to
        self.reminder_mode = reminder_mode


class ReminderLog(DataObject):
    __document_class__ = ReminderLogDocument

    def __init__(self, dbm, reminder=None, sent_status=None, number_of_sms=None, date=None, project_id=None,
                 to_number=""):
        DataObject.__init__(self, dbm)
        if reminder is not None:
            if reminder.reminder_mode == ReminderMode.ON_DEADLINE:
                reminder_mode = self._format_string_before_saving(reminder.reminder_mode)
            else:
                reminder_mode = str(reminder.day) + ' days ' + self._format_string_before_saving(reminder.reminder_mode)
            doc = ReminderLogDocument(reminder_id=reminder.id, project_id=project_id, sent_status=sent_status,
                                      number_of_sms=number_of_sms, date=date, message=reminder.message,
                                      remind_to=self._format_string_before_saving(to_number),
                                      reminder_mode=reminder_mode)
            DataObject._set_document(self, doc)

    @property
    def reminder_mode(self):
        return self._doc.reminder_mode

    @property
    def remind_to(self):
        return self._doc.remind_to

    @property
    def message(self):
        return self._doc.message

    @property
    def date(self):
        return self._doc.date

    def _format_string_before_saving(self, value):
        return (' '.join(value.split('_'))).title()





def get_simple_project_names(dbm):
    return [{'name': result['value']["name"], 'id': result['value']["id"]} for result in
            dbm.load_all_rows_in_view("simple_project_names")]


def count_projects(dbm, include_voided_projects=True):
    if include_voided_projects:
        rows = dbm.load_all_rows_in_view('count_projects', reduce=True, group_level=0)
    else:
        rows = dbm.load_all_rows_in_view('count_projects', reduce=True, group_level=1, key=False)

    return rows[0]['value'] - NUMBER_OF_NONPROJECT_FORMMODELS if not is_empty(rows) else 0


def delete_datasenders_from_project(manager, data_sender_ids):
    from datawinners.search.datasender_index import update_datasender_index_by_id

    for entity_id in data_sender_ids:
        associated_projects = get_all_projects(manager, data_sender_id=entity_id)
        for associated_project in associated_projects:
            project = Project.get(manager, associated_project['value']['_id'])
            project.delete_datasender(manager, entity_id)
            update_datasender_index_by_id(entity_id, manager)


def project_by_form_model_id(dbm, form_model_id):
    assert isinstance(dbm, DatabaseManager)
    assert is_string(form_model_id)
    rows = dbm.load_all_rows_in_view('project_by_form_model_id', key=form_model_id)
    if not len(rows):
        raise ProjectNotFoundException("project does not exist for form model id %s " % form_model_id)

    return Project._wrap_row(rows[0])


class ProjectNotFoundException(Exception):
    pass
