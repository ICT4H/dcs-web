import uuid

from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db import connection
from django.db.utils import IntegrityError

from datawinners import settings
from datawinners.feeds.database import feeds_db_for
from datawinners.main.database import get_db_manager
from datawinners.utils import get_database_manager_for_org
from datawinners.accountmanagement.models import Organization, OrganizationSetting
from datawinners.project.models import ProjectGuest, Project, PublicSurvey


class PublicProject():

    def __init__(self, questionnaire_id, id_generator):
        self.questionnaire_id = questionnaire_id
        self.id_generator = id_generator

    def _create_guest_entry(self, public_survey, email, name):
        project_guest = ProjectGuest.objects.create(public_survey=public_survey, guest_name=name, guest_email=email,
                                                   status=ProjectGuest.EMAIL_TO_BE_SEND,
                                                   link_id=str(self.id_generator.get_unique_id()))
        return project_guest

    def add_guest(self, public_survey, name, email):

        try:
            self._create_guest_entry(public_survey, email, name)
        except IntegrityError as ie:
            if 'guest_email' in ie.message:
                connection._rollback()
                return 'Email (%s) already added to survey'%email, False
            else:
                # retry once
                try:
                    self._create_guest_entry(public_survey, email, name)
                except Exception:
                    connection._rollback()
                    return 'Failed to add guest to survey', False

        return 'Guest added successfully to survey', True

    # def add_guests(self, guests):
    #     projectGuests = []
    #     for guest in guests:
    #         pass
    #     return 'Guest(s) added successfully to survey', True

    def remove_guests(self, guests):
        pass


class GuestFinder():

    def get_all_guest_for_survey(self, org_id, questionnaire_id):
        public_survey = PublicSurvey.objects.filter(organization=org_id, questionnaire_id=questionnaire_id)
        if len(public_survey) < 1:
            return []

        projectGuests = public_survey[0].projectguest_set.all()
        data = []
        for pgs in projectGuests:
            data.append([pgs.id, pgs.guest_name, pgs.guest_email])

        return data

    def get_paginated_guest_for_survey(self, questionnaire_id, start, count):
        pass


class GuestMapper():

    def get_guest_from_form(self, data):
        projectGuest = ProjectGuest()
        projectGuest.guest_name = data.get('name', '')
        projectGuest.email = data.get('email', '')

        try:
            projectGuest.save()
            success = True
            message = 'Guest successfully added to the project'
        except Exception as e:
            message = e.message

class GuestEmail():

    def __init__(self, domain, subject_line=None):
        self.domain = domain
        self.subject_line = '- ' + subject_line if subject_line else ''

    def sendEmails(self, guest_ids):
        guests = ProjectGuest.objects.filter(pk__in=[int(entry) for entry in guest_ids])

        for guest in guests:
            self._send_mail(guest.guest_email, guest.link_id)
            guest.mark_email_send()

        return len(guests)

    def _send_mail(self, guest_email, link_id):
        language = 'en'
        context = {
            'domain': self.domain,
            'link_id': link_id
        }
        subject = render_to_string('registration/guest_survey_email_subject_in_'+language+'.txt')
        subject = ''.join(subject.splitlines()) + self.su# Email subject *must not* contain newlines
        message = render_to_string('registration/guest_survey_link_email_'+language+'.html',
                                   context)
        email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [guest_email], [settings.HNI_SUPPORT_EMAIL_ID])
        email.content_subtype = "html"
        email.send()

class UniqueIdGenerator():

    def get_unique_id(self):
        return uuid.uuid4()


class GuestSearch():

    def findGuestsByQuestionnaireId(self):
        pass

class PublicSubmission():
    def mark_submitted(self, link_url):
        pass

    def get_organisation(self):
        return self.organization

    def get_questionnaire(self):
        return self.questionnaire

    def get_dbm(self):
        return self.dbm

    def get_feeds_dbm(self):
        return self.feeds_dbm

    def get_form_code(self):
        return self.questionnaire.form_code;

class GuestSubmission(PublicSubmission):

    def __init__(self, link_id):
        projectGuestObjects = ProjectGuest.objects.filter(link_id=link_id)
        if len(projectGuestObjects) < 1:
            raise InvalidLinkException()
        self.project_guest = projectGuestObjects[0]
        if self.project_guest.status == ProjectGuest.SURVEY_TAKEN:
            raise SubmissionTakenError
        if self.project_guest.status != ProjectGuest.EMAIL_SEND:
            raise InvalidLinkException

        #TODO raise survey expired exception
        settings = OrganizationSetting.objects.get(organization=self.project_guest.public_survey.organization)
        self.dbm = get_db_manager(settings.document_store)
        self.feeds_dbm = feeds_db_for(settings.document_store)
        self.questionnaire = Project.get(self.dbm, self.project_guest.public_survey.questionnaire_id)
        self.organization = self.project_guest.public_survey.organization

    def get_guest_email(self):
        return self.project_guest.guest_email

    def mark_submission_taken(self):
        self.project_guest.mark_submission_taken()

class AnonymousSubmission(PublicSubmission):

    def __init__(self, org_id, anonymous_link_id):
        public_survey_objects = PublicSurvey.objects.filter(organization=org_id, anonymous_link_id=anonymous_link_id)
        if len(public_survey_objects) < 1:
            raise InvalidLinkException()
        self.public_survey = public_survey_objects[0]

        #TODO raise survey expired and allowed count exceptions
        settings = OrganizationSetting.objects.get(organization=self.public_survey.organization)
        self.dbm = get_db_manager(settings.document_store)
        self.feeds_dbm = feeds_db_for(settings.document_store)
        self.questionnaire = Project.get(self.dbm, self.public_survey.questionnaire_id)
        self.organization = self.public_survey.organization

    def mark_submission_taken(self):
        self.public_survey.mark_submission_taken()

class InvalidLinkException(Exception):
    pass

class SubmissionTakenError(Exception):
    pass

class GuestDatabaseManager():

    def __init__(self, org_id):
        self.org_id = org_id
        self.organization = Organization.objects.filter(pk=org_id)
        self.dbm = get_database_manager_for_org(self.organization)

    def get_dbm(self):
        return self.dbm

