import json
from django.contrib import messages
from django.http import HttpResponseBadRequest, HttpResponse
from django.template.loader import render_to_string
from django.utils.translation import ugettext
from datawinners.accountmanagement.models import NGOUserProfile, Organization, get_ngo_admin_user_profiles_for
from datawinners.feeds.database import get_feeds_database
from datawinners.feeds.mail_client import mail_feed_errors
from datawinners.main.database import get_database_manager
from datawinners.messageprovider.messages import WEB
from datawinners.project.views.datasenders import _get_domain
from datawinners.search.submission_index import UNKNOWN
from datawinners.submission.views import check_quotas_and_update_users, check_quotas_for_trial
from datawinners.xforms.views import sp_submission_logger, logger, get_errors, is_authorized_for_questionnaire
from mangrove.form_model.form_model import get_form_model_by_code
from mangrove.transport import Request, TransportInfo
from mangrove.errors.MangroveException import ExceedSMSLimitException
from mangrove.transport.player.new_players import XFormPlayerV2
from mangrove.transport.repository.survey_responses import get_survey_response_by_id
from mangrove.utils.dates import py_datetime_to_js_datestring
from django.core.mail import EmailMessage
from datawinners import settings
class XFormWebSubmissionHandler():

    def __init__(self, request, form_code=None):
        self.request = request
        self.request_user = request.user
        self.manager = get_database_manager(self.request_user)
        self.player = XFormPlayerV2(self.manager, get_feeds_database(self.request_user))
        self.xml_submission_file = request.POST['form_data']
        self.retain_files = request.POST['retain_files'].split(',') if request.POST.get('retain_files') else None

        self.user_profile = NGOUserProfile.objects.get(user=self.request_user)
        self.mangrove_request = Request(message=self.xml_submission_file, media=request.FILES,
            retain_files=self.retain_files,
            transportInfo=
            TransportInfo(transport=WEB,
                source=self.request_user.email,
                destination=''
            ))
        self.form_code = form_code if form_code else self.request.POST['form_code']
        self.organization = Organization.objects.get(org_id=self.user_profile.org_id)

    def create_new_submission_response(self):
        try:
            if not is_authorized_for_questionnaire(self.manager, self.request_user, self.form_code):
                return HttpResponse(status=403)
            if self.organization.in_trial_mode:
                check_quotas_for_trial(self.organization)
        except Exception as e:
            if not isinstance(e, ExceedSMSLimitException):
                raise e
        player_response = self.player.add_survey_response(self.mangrove_request, self.user_profile.reporter_id,
                                                          logger=sp_submission_logger)
        return self._post_save(player_response)

    def update_submission_response(self, survey_response_id):

        if not is_authorized_for_questionnaire(self.manager, self.request_user, self.form_code):
            return HttpResponse(status=403)

        survey_response = get_survey_response_by_id(self.manager, survey_response_id)
        if not survey_response:
            raise LookupError()

        player_response = self.player.update_survey_response(self.mangrove_request,
                                                      logger=sp_submission_logger, survey_response=survey_response)
        return self._post_save(player_response)

    def _post_save(self, response):
        mail_feed_errors(response, self.manager.database_name)
        if response.errors:
            logger.error("Error in submission : \n%s" % get_errors(response.errors))
            messages.error(self.request, ugettext('Submission failed %s' % get_errors(response.errors)), extra_tags='error')
            return HttpResponseBadRequest()

        self.organization.increment_message_count_for(incoming_web_count=1)
        content = json.dumps({'submission_uuid': response.survey_response_id,
                              'version': response.version,
                              'created': py_datetime_to_js_datestring(response.created)})
        success_response = HttpResponse(content, status=201, content_type='application/json')
        success_response['submission_id'] = response.survey_response_id
        messages.success(self.request, ugettext('Successfully submitted'), extra_tags='success')

        check_quotas_and_update_users(self.organization)
        return success_response


class PublicWebSubmissionHandler(XFormWebSubmissionHandler):

    def __init__(self, request, public_submission):
        self.public_submission = public_submission
        self.request = request
        self.manager = public_submission.get_dbm()
        self.organization = public_submission.get_organisation()
        self.player = XFormPlayerV2(self.manager, public_submission.get_feeds_dbm())

        self.xml_submission_file = request.POST['form_data']
        self.retain_files = request.POST['retain_files'].split(',') if request.POST.get('retain_files') else None

        form_code = public_submission.get_form_code()
        self.form_code = form_code if form_code else self.request.POST['form_code']

    def _get_mangrove_request(self):
        return Request(message=self.xml_submission_file, media=self.request.FILES,
            retain_files=self.retain_files,
            transportInfo=
            TransportInfo(transport=WEB,
                source=UNKNOWN,
                destination=''
            ))

    def create_new_guest_submission(self):
        if self.public_submission.public_survey.submissions_count >= self.public_submission.public_survey.allowed_submission_count:
            return HttpResponse(content="Public survey limit reach", status=400)
        player_response = self.player.add_guest_survey_response(self._get_mangrove_request(), logger=sp_submission_logger)
        self.public_submission.mark_submission_taken()
        if self.public_submission.public_survey.get_remaining_submission_count() == 50:
            self._send_limit_reaching_email()
        return self._post_save(player_response)

    def _send_limit_reaching_email(self):
        admins = get_ngo_admin_user_profiles_for(self.organization)
        language = 'en'
        form_model = get_form_model_by_code(self.manager, self.form_code)
        for admin in admins:
            ctx_dict = {'domain': _get_domain(self.request) ,
                        'username': admin.user.first_name,
                        'project_name': form_model.name}
            subject = render_to_string('registration/submission_limit_subject_'+language+'.txt')
            subject = ''.join(subject.splitlines()) # Email subject *must not* contain newlines
            message = render_to_string('registration/submission_limit_email_'+language+'.html', ctx_dict)
            email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [admin.user.email], [settings.HNI_SUPPORT_EMAIL_ID])
            email.content_subtype = "html"
            email.send()

class GuestWebSubmissionHandler(PublicWebSubmissionHandler):

    def _get_mangrove_request(self):
        return Request(message=self.xml_submission_file, media=self.request.FILES,
            retain_files=self.retain_files,
            transportInfo=
            TransportInfo(transport=WEB,
                source=self.public_submission.get_guest_email(),
                destination=''
            ))

