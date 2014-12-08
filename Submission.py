import json
from datetime import datetime
from django.utils.translation import get_language, ugettext

from datawinners.search.index_utils import es_unique_id_code_field_name, es_questionnaire_field_name
from datawinners.search.query import Query
from datawinners.search.submission_headers import HeaderFactory
from datawinners.search.submission_index_constants import SubmissionIndexConstants
from datawinners.search.submission_query import SubmissionQueryBuilder
from mangrove.form_model.field import FieldSet
from mangrove.utils.dates import py_datetime_to_js_datestring


class SubmissionQueryMobile(Query):
    HEADER_FOR = "mobile"
    def __init__(self, form_model, query_params):
        Query.__init__(self, SubmissionQueryMobileResponseCreator(form_model), SubmissionQueryBuilder(form_model),
                       query_params)
        self.form_model = form_model

    def get_headers(self, entity_type, user):
        headers = self.query_params['headers'] if self.query_params.get('headers', None) else \
            HeaderFactory(self.form_model).create_header(self.HEADER_FOR).get_header_field_names()
        return headers

    def add_unique_id_field(self, unique_id_field, header_dict):
        return None

    def get_header_dict(self):
        header = HeaderFactory(self.form_model).create_header(self.HEADER_FOR)

        return header.get_header_field_dict()

    def query(self, database_name):
        query_all_results = self.query_builder.query_all(database_name, self.form_model.id)
        # take all headers if nothing selected
        headers = HeaderFactory(self.form_model).create_header(self.HEADER_FOR)
        submission_headers = headers
        query_by_submission_type = self.query_builder.filter_by_submission_type(query_all_results, self.query_params)
        filtered_query = self.query_builder.add_query_criteria(submission_headers, query_by_submission_type,
                                                               self.query_params.get('search_filters').get(
                                                                   'search_text'),
                                                               query_params=self.query_params)
        submissions = self.response_creator.create_response(submission_headers, filtered_query)
        return submissions

class SubmissionQueryMobileResponseCreator():
    def __init__(self, form_model):
        self.form_model = form_model

    def combine_name_and_id(self, short_code, entity_name):
        return ["%s<span class='small_grey'>  %s</span>" % (entity_name, short_code)] if entity_name else entity_name

    def get_field_set_fields(self,fields):
        field_set_field_dict = {}
        for field in fields:
            if(isinstance(field,FieldSet)):
              field_set_field_dict.update({es_questionnaire_field_name(field.code,self.form_model.id):field})
              field_set_field_dict.update(self.get_field_set_fields(field.fields))
        return field_set_field_dict

    def create_response(self, required_field_names, query):
        entity_question_codes = [es_questionnaire_field_name(field.code, self.form_model.id) for field in
                                 self.form_model.entity_questions]
        fieldset_fields = self.get_field_set_fields(self.form_model.fields)
        meta_fields = [SubmissionIndexConstants.DATASENDER_ID_KEY]
        meta_fields.extend([es_unique_id_code_field_name(code) for code in entity_question_codes])

        submissions = []
        language = get_language()
        for res in query.values_dict(tuple(required_field_names)):
            submission = {'id': [res._id]}
            for key in required_field_names:
                if not key in meta_fields:
                    #TODO do we need entity_question
                    if key in entity_question_codes:
                        submission[key] = self.combine_name_and_id(short_code=res.get(es_unique_id_code_field_name(key)),
                                                 entity_name=res.get(key))
                    elif key == SubmissionIndexConstants.DATASENDER_NAME_KEY:
                        submission[key] = self.combine_name_and_id(res.get(SubmissionIndexConstants.DATASENDER_ID_KEY),
                                                 res.get(SubmissionIndexConstants.DATASENDER_NAME_KEY))
                    elif key == 'status':
                        submission[key] = ugettext(res.get(key))
                    elif key == 'error_msg':
                        error_msg = res.get(key)
                        if error_msg.find('| |') != -1:
                            error_msg = error_msg.split('| |,')[['en', 'fr'].index(language)]
                        submission[key] = error_msg
                    elif key == "date":
                        created_date_time = datetime.strptime(res.get(key), '%b. %d, %Y, %I:%M %p')
                        submission[key.split('_', 1)[-1]] = py_datetime_to_js_datestring(created_date_time)
                    elif key in fieldset_fields.keys():
                        submission[key.split('_', 1)[-1]] = json.loads(res.get(key))
                    else:
                        submission[key.split('_', 1)[-1]] = res.get(key)
            submissions.append(submission)
        return submissions
