import json
import os
from string import lower
from urllib import unquote
import unicodedata

from django.contrib.sites.models import Site, RequestSite
from django.contrib.auth.decorators import login_required
from django import forms
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import translation
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_view_exempt, csrf_response_exempt
from django.views.generic.base import View
import jsonpickle
from datawinners.entity.entity_exceptions import InvalidFileFormatException
from datawinners.entity.import_data import get_filename_and_contents

from datawinners.utils import get_organization
from datawinners import settings
from datawinners.accountmanagement.decorators import is_not_expired, session_not_expired, is_datasender
from datawinners.activitylog.models import UserActivityLog
from datawinners.common.constant import IMPORTED_DATA_SENDERS
from datawinners.entity import import_data as import_module
from datawinners.entity.datasender_tasks import convert_open_submissions_to_registered_submissions, \
    update_datasender_on_open_submissions
from datawinners.entity.helper import rep_id_name_dict_of_users
from datawinners.main.database import get_database_manager
from datawinners.project.helper import is_project_exist
from datawinners.project.models import Project, get_or_create_public_survey_of, PublicSurvey, ProjectGuest
from datawinners.project.public_project_guest_handler import GuestEmail, PublicProject, GuestFinder, UniqueIdGenerator
from datawinners.project.views.views import get_project_link, _in_trial_mode, _is_pro_sms
from datawinners.search.datasender_index import update_datasender_index_by_id
from datawinners.search.entity_search import MyDataSenderQuery
from mangrove.form_model.project import Project
from mangrove.transport.player.parser import XlsDatasenderParser
from mangrove.utils.types import is_empty
from datawinners.project.utils import is_quota_reached


class MyDataSendersAjaxView(View):
    def strip_accents(self, s):
        return ''.join((c for c in unicodedata.normalize('NFD', unicode(s)) if unicodedata.category(c) != 'Mn'))

    def post(self, request, project_name, *args, **kwargs):
        search_parameters = {}
        search_text = lower(request.POST.get('sSearch', '').strip())
        search_parameters.update({"search_text": search_text})
        search_parameters.update({"start_result_number": int(request.POST.get('iDisplayStart'))})
        search_parameters.update({"number_of_results": int(request.POST.get('iDisplayLength'))})
        search_parameters.update({"order_by": int(request.POST.get('iSortCol_0')) - 1})
        search_parameters.update({"order": "-" if request.POST.get('sSortDir_0') == "desc" else ""})

        user = request.user
        project_name_unquoted = lower(unquote(project_name))
        query_count, search_count, datasenders = MyDataSenderQuery(search_parameters).filtered_query(user,
                                                                                                     self.strip_accents(
                                                                                                         project_name_unquoted),
                                                                                                     search_parameters)

        return HttpResponse(
            jsonpickle.encode(
                {
                    'data': datasenders,
                    'iTotalDisplayRecords': query_count,
                    'iDisplayStart': int(request.POST.get('iDisplayStart')),
                    "iTotalRecords": search_count,
                    'iDisplayLength': int(request.POST.get('iDisplayLength'))
                }, unpicklable=False), content_type='application/json')

    @method_decorator(csrf_view_exempt)
    @method_decorator(csrf_response_exempt)
    @method_decorator(login_required)
    @method_decorator(session_not_expired)
    @method_decorator(is_not_expired)
    def dispatch(self, *args, **kwargs):
        return super(MyDataSendersAjaxView, self).dispatch(*args, **kwargs)


def parse_successful_imports(successful_imports):
    imported_data_senders = []

    if not successful_imports:
        return imported_data_senders

    for successful_import in successful_imports.values():
        data_sender = {}
        data_sender['email'] = successful_import["email"] if "email" in successful_import else ""
        data_sender['location'] = ",".join(successful_import["l"]) if "l" in successful_import else ""
        data_sender['coordinates'] = ','.join(
            str(coordinate) for coordinate in successful_import["g"]) if 'g' in successful_import else ""
        data_sender['name'] = successful_import['n']
        data_sender['mobile_number'] = successful_import['m']
        data_sender['id'] = successful_import['s']
        imported_data_senders.append(data_sender)
    return imported_data_senders


def _add_imported_datasenders_to_project(imported_datasenders_id, manager, project):
    project.data_senders.extend(imported_datasenders_id)
    project.save(process_post_update=False)
    for datasender_id in imported_datasenders_id:
        update_datasender_index_by_id(datasender_id, manager)




@login_required
@csrf_exempt
@is_not_expired
@is_project_exist
@is_datasender
def registered_datasenders(request, project_id):
    manager = get_database_manager(request.user)
    questionnaire = Project.get(manager, project_id)
    project_links = get_project_link(questionnaire)
    dashboard_page = settings.HOME_PAGE + "?deleted=true"
    if questionnaire.is_void():
        return HttpResponseRedirect(dashboard_page)
    if request.method == 'GET':
        in_trial_mode = _in_trial_mode(request)
        is_open_survey_allowed = _is_pro_sms(request) and not questionnaire.xform
        is_open_survey = 'open' if questionnaire.is_open_survey else 'restricted'
        user_rep_id_name_dict = rep_id_name_dict_of_users(manager)
        return render_to_response('project/registered_datasenders.html',
                                  {'project': questionnaire,
                                   'project_links': project_links,
                                   'questionnaire_code': questionnaire.form_code,
                                   'current_language': translation.get_language(),
                                   'is_quota_reached': is_quota_reached(request),
                                   'in_trial_mode': in_trial_mode,
                                   'is_open_survey_allowed': is_open_survey_allowed,
                                   'is_open_survey': is_open_survey,
                                   'user_dict': json.dumps(user_rep_id_name_dict)},
                                  context_instance=RequestContext(request))
    if request.method == 'POST':
        error_message, failure_imports, success_message, successful_imports = import_module.import_data(request,
                                                                                                        manager,
                                                                                                        default_parser=XlsDatasenderParser)
        imported_data_senders = parse_successful_imports(successful_imports)
        imported_datasenders_ids = [imported_data_sender["id"] for imported_data_sender in imported_data_senders]
        _add_imported_datasenders_to_project(imported_datasenders_ids, manager, questionnaire)
        convert_open_submissions_to_registered_submissions.delay(manager.database_name, imported_datasenders_ids)

        if len(imported_datasenders_ids):
            UserActivityLog().log(request, action=IMPORTED_DATA_SENDERS,
                                  detail=json.dumps(dict({"Unique ID": "[%s]" % ", ".join(imported_datasenders_ids)})),
                                  project=questionnaire.name)
        return HttpResponse(json.dumps(
            {
                'success': error_message is None and is_empty(failure_imports),
                'message': success_message,
                'error_message': error_message,
                'failure_imports': failure_imports,
                'successful_imports': imported_data_senders
            }))

@csrf_exempt
@login_required
@is_not_expired
def delete_project_guests(request, project_id):
    if request.method == 'POST':
        publicProject = PublicProject(project_id)
        org = get_organization(request)
        selected_project_guest_ids = _get_selected_guest_ids(request, org.org_id, project_id)
        publicProject.delete_guests(selected_project_guest_ids)

        return HttpResponse(
            jsonpickle.encode({
                'success': True,
                'success_message': "Guest deleted from survey."
            })
        )


def _get_selected_guest_ids(request, org_id, project_id):
    selected_project_guest_ids = json.loads(request.POST.get('id_list', []))
    all_selected = request.POST.get('all_selected', None)
    if all_selected == 'true':
        email_status_filter = request.POST.get('email_status_filter', '')
        email_status = None if email_status_filter == 'all' else int(email_status_filter)
        if email_status:
            guests = ProjectGuest.objects.filter(public_survey__organization=org_id,
                                             public_survey__questionnaire_id=project_id,
                                             status=email_status)
        else:
            guests = ProjectGuest.objects.filter(public_survey__organization=org_id,
                                             public_survey__questionnaire_id=project_id)

        selected_project_guest_ids = [guest.id for guest in guests]

    return selected_project_guest_ids


@csrf_exempt
@login_required
@is_not_expired
def project_guests_send_email(request, project_id):
    if request.method == 'POST':
        org = get_organization(request)
        selected_project_guest_ids = _get_selected_guest_ids(request, org.org_id, project_id)

        public_survey = PublicSurvey.objects.filter(organization=org, questionnaire_id=project_id)[0]
        emailer = GuestEmail(_get_domain(request), public_survey)
        success_count = emailer.send_emails(selected_project_guest_ids);
        return HttpResponse(
            jsonpickle.encode({
                'success': True,
                'success_message': "Survey request send to %s guest(s)"% success_count
            })
        )


def _get_domain(request):
    if Site._meta.installed:
        return Site.objects.get_current().domain
    else:
        return RequestSite(request).domain

@csrf_exempt
@login_required
@is_not_expired
def project_guests(request, project_id):
    if request.method == 'POST':
        organisation = get_organization(request)
        guest_finder = GuestFinder()

        iDisplayStart = int(request.POST.get('iDisplayStart'))
        iDisplayLength = int(request.POST.get('iDisplayLength'))
        email_status_req = request.POST.get('email_status')
        email_status = -1 if email_status_req == 'undefined' or email_status_req == 'all' else int(email_status_req)

        current_page = 1 if iDisplayStart == 0 else (iDisplayStart / iDisplayLength) + 1

        search_count, guests_data = guest_finder.get_paginated_guest_for_survey(organisation.org_id, project_id,
                                                                            email_status, current_page, iDisplayLength)
        query_count = len(guests_data)

        return HttpResponse(
        jsonpickle.encode(
            {
                'data': guests_data,
                'iTotalDisplayRecords': search_count,
                'iDisplayStart': int(request.POST.get('iDisplayStart')),
                "iTotalRecords": query_count,
                'iDisplayLength': int(request.POST.get('iDisplayLength', 0))
            }, unpicklable=False), content_type='application/json')

class PublicProjectForm(forms.Form):
    email_subject = forms.CharField(required=False)
    email_body = forms.CharField(widget=forms.Textarea, required=False)
    custom_brand_logo = forms.CharField(required=False)
    band_color = forms.CharField(required=False)
    is_anonymous_enabled = forms.BooleanField(initial=False, required=False, widget=forms.CheckboxInput(attrs={'data-bind': 'checked: is_anonymous_enabled'}))
    allowed_submission_count = forms.IntegerField(initial=-1, required=False)
    expires_on = forms.DateField(widget=forms.widgets.DateInput(format='%d.%m.%Y'), input_formats=['%d.%m.%Y'], required=False)
    public_link = forms.CharField(max_length=100, required=False)


class ProjectGuestForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(max_length=100)

@csrf_exempt
@login_required
@is_not_expired
def public_survey(request, project_id):
    manager = get_database_manager(request.user)
    questionnaire = Project.get(manager, project_id)
    project_links = get_project_link(questionnaire)
    success = False
    message = ''
    domain = _get_domain(request)
    organisation = get_organization(request)
    public_survey = get_or_create_public_survey_of(questionnaire.id, organisation.org_id, questionnaire.name)

    if request.method == 'POST':
        form = PublicProjectForm(request.POST)
        if form.is_valid():
            form_data = form.cleaned_data
            public_survey.allowed_submission_count = 1000 if form_data['allowed_submission_count'] is None else form_data['allowed_submission_count']
            public_survey.anonymous_web_submission_allowed = form_data['is_anonymous_enabled']
            public_survey.email_subject = form_data['email_subject']
            public_survey.email_body = form_data['email_body']
            public_survey.custom_brand_logo = form_data['custom_brand_logo']
            public_survey.band_color = form_data['band_color']
            public_survey.survey_expiry_date = form_data['expires_on']
            public_survey.save()
            success, message = True, 'Survey settings updated'
    else:
        form = PublicProjectForm({'public_link': public_survey.anonymous_link_id,
                                  'email_subject': public_survey.email_subject,
                                  'email_body': public_survey.email_body,
                                  'custom_brand_logo': public_survey.custom_brand_logo,
                                  'band_color': public_survey.band_color,
                                  'is_anonymous_enabled': public_survey.anonymous_web_submission_allowed,
                                  'expires_on': public_survey.survey_expiry_date,
                                  'allowed_submission_count': public_survey.allowed_submission_count})

    return render_to_response('project/public_survey.html',
      {'project': questionnaire,
       'domain': domain,
       'public_link': public_survey.anonymous_link_id,
       'org_id': organisation.org_id,
       'project_links': project_links,
       'success': success,
       'message': message,
       'questionnaire_code': questionnaire.form_code,
       'current_language': translation.get_language(),
       'is_quota_reached': is_quota_reached(request),
       'form': form},
      context_instance=RequestContext(request))

@csrf_exempt
@login_required
@is_not_expired
def add_project_guests(request, project_id):
    manager = get_database_manager(request.user)
    questionnaire = Project.get(manager, project_id)
    project_links = get_project_link(questionnaire)
    success = False
    message = ''

    if request.method == 'POST':
        guest_form = ProjectGuestForm(request.POST)
        if guest_form.is_valid():
            organisation = get_organization(request)
            public_survey = get_or_create_public_survey_of(questionnaire.id, organisation.org_id, questionnaire.name)

            public_project = PublicProject(project_id, public_survey, UniqueIdGenerator())
            message, success = public_project.add_guest(
                guest_form.cleaned_data.get('name', ''),
                guest_form.cleaned_data.get('email', ''))
    else:
        guest_form = ProjectGuestForm()

    return render_to_response('project/project_guests.html',
      {'project': questionnaire,
       'project_links': project_links,
       'success': success,
       'message': message,
       'questionnaire_code': questionnaire.form_code,
       'current_language': translation.get_language(),
       'is_quota_reached': is_quota_reached(request),
       'guest_form': guest_form},
      context_instance=RequestContext(request))

@csrf_exempt
@login_required
@is_not_expired
def import_guest(request, project_id):
    manager = get_database_manager(request.user)
    questionnaire = Project.get(manager, project_id)
    organisation = get_organization(request)
    success, message = True, 'Guest(s) added successfully to survey. '\
        'Use the \'Send survey email\' from the Actions to email survey link to selected guest(s)'
    public_survey = get_or_create_public_survey_of(questionnaire.id, organisation.org_id, questionnaire.name)
    public_project = PublicProject(project_id, public_survey, UniqueIdGenerator())

    try:
        file_content = _get_uploaded_content(request)
        duplicate_emails = public_project.import_guests(file_content)
        if len(duplicate_emails) > 0:
                success, message = False, 'Error: Remove the following duplicate guest(s) and upload again.<br>' +\
                                  '<br>'.join(duplicate_emails)
    except InvalidFileFormatException:
        success, message = False, 'Invalid file format'
    except Exception:
        success, message = False, 'Something unexpected happened; please check the file data and try again'

    return HttpResponse(
            json.dumps(
                {
                    "success": success,
                    "message": message
                }))

def _get_uploaded_content(request):
    file_name, file_content = get_filename_and_contents(request)
    base_name, extension = os.path.splitext(file_name)
    if extension != '.xls':
        raise InvalidFileFormatException()

    return file_content