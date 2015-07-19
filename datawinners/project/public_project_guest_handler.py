from gettext import gettext
import uuid

from django.core.mail import EmailMessage
from django.core.paginator import Paginator
from django.template import Template, Context
from django.template.loader import render_to_string
from django.db import connection, transaction
from django.db.utils import IntegrityError
from rest_framework.reverse import reverse

from datawinners import settings
from datawinners.feeds.database import feeds_db_for
from datawinners.main.database import get_db_manager
from datawinners.project.submission.submission_import import XlsSubmissionParser, ImportValidationError
from datawinners.utils import get_database_manager_for_org
from datawinners.accountmanagement.models import Organization, OrganizationSetting, get_ngo_admin_user_profiles_for
from datawinners.project.models import ProjectGuest, Project, PublicSurvey
from mangrove.form_model.form_model import get_form_model_by_code


class PublicProject():

    def __init__(self, questionnaire_id, public_survey=None, id_generator=None):
        self.questionnaire_id = questionnaire_id
        self.id_generator = id_generator
        self.public_survey = public_survey

    def _create_guest_entry(self, email, name):
        assert self.id_generator is not None
        assert self.public_survey is not None
        project_guest = ProjectGuest.objects.create(public_survey=self.public_survey, guest_name=name,
                                                    guest_email=email.lower(), # email is converted to lower case
                                                    status=ProjectGuest.EMAIL_TO_BE_SEND,
                                                    link_id=str(self.id_generator.get_unique_id()))
        return project_guest

    def add_guest(self, name, email):

        try:
            self._create_guest_entry(email, name)
        except IntegrityError as ie:
            if 'guest_email' in ie.message:
                connection._rollback()
                return 'Email (%s) already added to survey'%email, False
            else:
                # retry once
                try:
                    self._create_guest_entry(self.public_survey, email, name)
                except Exception:
                    connection._rollback()
                    return 'Failed to add guest to survey', False

        return 'Guest added successfully to survey. '\
            'Use the \'Send survey email\' from the Actions to email survey link to selected guest(s)', True

    # def add_guests(self, guests):
    #     projectGuests = []
    #     for guest in guests:
    #         pass
    #     return 'Guest(s) added successfully to survey', True

    def delete_guests(self, selected_project_guest_ids):
        ProjectGuest.objects.filter(pk__in=[int(entry) for entry in selected_project_guest_ids]).delete()

    def import_guests(self, file_content):
        tabular_data = XlsSubmissionParser().parse(file_content)
        if len(tabular_data) < 1:
            raise ImportValidationError(gettext("The imported file is empty."))
        return self._add_guests(self._strip_header_row(tabular_data))

    def _strip_header_row(self, tabular_data):
        if tabular_data[0][0].lower() == 'email':
            return tabular_data[1:]
        else:
            return tabular_data

    def _add_guests(self, guests_info):
        duplicate_emails = []
        with transaction.commit_manually():
            for info in guests_info:
                email, name = self._name_email_safe_get(info)
                try:
                    self._create_guest_entry(email, name)
                except IntegrityError as ie:
                    if 'guest_email' in ie.message:
                        connection._rollback()
                        duplicate_emails.append(email)
            if len(duplicate_emails) == 0:
                transaction.commit()
            else:
                transaction.rollback()

        return duplicate_emails

    def _name_email_safe_get(self, guest_info):
        if (len(guest_info) == 2):
            return guest_info[0], guest_info[1]
        else:
            return guest_info[0], ''


class GuestFinder():

    def get_all_guest_for_survey(self, org_id, questionnaire_id):
        public_survey = PublicSurvey.objects.filter(organization=org_id, questionnaire_id=questionnaire_id)
        if len(public_survey) < 1:
            return []

        project_guests = public_survey[0].projectguest_set.all()
        data = self._transform_to_array(project_guests)

        return data

    def get_paginated_guest_for_survey(self, org_id, questionnaire_id, email_status, page_num, count):
        if email_status > -1:
            guests = ProjectGuest.objects.filter(public_survey__organization=org_id,
                                             public_survey__questionnaire_id=questionnaire_id,
                                             status=email_status)
        else:
            guests = ProjectGuest.objects.filter(public_survey__organization=org_id,
                                             public_survey__questionnaire_id=questionnaire_id)
        if len(guests) < 1:
            return 0, []

        page = Paginator(guests, count)
        project_guests = page.page(page_num).object_list
        return page.count, self._transform_to_array(project_guests)

    def _transform_to_array(self, project_guests):
        data = []

        for pgs in project_guests:
            data.append([pgs.id, pgs.guest_name, pgs.guest_email, pgs.get_status_label()])
        return data


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

    def __init__(self, domain, public_survey):
        self.domain = domain
        self.public_survey = public_survey
        self.email_body_template = Template(self.public_survey.email_body)


    def send_emails(self, project_guest_ids):
        guests = ProjectGuest.objects.filter(pk__in=[int(entry) for entry in project_guest_ids])
        for guest in guests:
            self._send_mail(guest)
            guest.mark_email_send()

        return len(guests)

    def _send_mail(self, guest):
        context = Context({
            'name': guest.guest_name,
            'email_subject': self.public_survey.email_subject,
            'domain': self.domain,
            'survey_link': 'https://%s%s'%(self.domain, reverse('guest_survey', args=[guest.link_id]), )
        })
        message = self.email_body_template.render(context)
        email = EmailMessage(self.public_survey.email_subject, message, settings.DEFAULT_FROM_EMAIL, [guest.guest_email], [settings.HNI_SUPPORT_EMAIL_ID])
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

    def post_save(self):
        pass


class GuestSubmission(PublicSubmission):

    def __init__(self, link_id):
        project_guest_objects = ProjectGuest.objects.filter(link_id=link_id)
        if len(project_guest_objects) < 1:
            raise InvalidLinkException()
        self.project_guest = project_guest_objects[0]
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

        if self.public_submission.public_survey.submissions_count >=\
                self.public_submission.public_survey.allowed_submission_count:
            raise AllowedSubmissionLimitException()
        #TODO raise survey expired

        settings = OrganizationSetting.objects.get(organization=self.public_survey.organization)
        self.dbm = get_db_manager(settings.document_store)
        self.feeds_dbm = feeds_db_for(settings.document_store)
        self.questionnaire = Project.get(self.dbm, self.public_survey.questionnaire_id)
        self.organization = self.public_survey.organization

    def mark_submission_taken(self):
        self.public_survey.mark_submission_taken()

    def post_save(self):
        if self.public_submission.public_survey.get_remaining_submission_count() == 50:
            self._send_limit_nearing_email()

    def _send_limit_nearing_email(self):
        admins = get_ngo_admin_user_profiles_for(self.organization)
        language = 'en'
        form_model = get_form_model_by_code(self.manager, self.form_code)
        for admin in admins:
            ctx_dict = {'username': admin.user.first_name,
                        'project_name': form_model.name}
            subject = render_to_string('registration/submission_limit_subject_'+language+'.txt')
            subject = ''.join(subject.splitlines()) # Email subject *must not* contain newlines
            message = render_to_string('registration/submission_limit_email_'+language+'.html', ctx_dict)
            email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [admin.user.email], [settings.HNI_SUPPORT_EMAIL_ID])
            email.content_subtype = "html"
            email.send()


class InvalidLinkException(Exception):
    pass

class AllowedSubmissionLimitException(Exception):
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

