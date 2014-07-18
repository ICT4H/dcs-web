from django.utils.translation import get_language, ugettext
from datawinners.search.index_utils import es_field_name, es_unique_id_code_field_name
from datawinners.search.query import Query
from datawinners.search.submission_headers import HeaderFactory
from datawinners.search.submission_index_constants import SubmissionIndexConstants
from datawinners.search.submission_query import SubmissionQueryBuilder


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
        #{k,v for k1,v1 in header}

        return header.get_header_field_dict()

    def query(self, database_name):
        query_all_results = self.query_builder.query_all(database_name, self.form_model.id)

        # take all headers if nothing selected

        # headers = ["4934e8e8072d11e4ae2b001c42af7554_your_name"]#self.query_params.get('headers')
        headers = HeaderFactory(self.form_model).create_header(self.HEADER_FOR)
        # submission_headers = header.get_header_field_names()
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

    def create_response(self, required_field_names, query):
        entity_question_codes = [es_field_name(field.code, self.form_model.id) for field in
                                 self.form_model.entity_questions]
        meta_fields = [SubmissionIndexConstants.DATASENDER_ID_KEY]
        meta_fields.extend([es_unique_id_code_field_name(code) for code in entity_question_codes])

        submissions = []
        language = get_language()
        for res in query.values_dict(tuple(required_field_names)):
            submission = [res._id]
            for key in required_field_names:
                if not key in meta_fields:
                    #TODO do we need entity_question
                    if key in entity_question_codes:
                        self.combine_name_and_id(short_code=res.get(es_unique_id_code_field_name(key)),
                                                 entity_name=res.get(key), submission=submission)
                    elif key == 'status':
                        submission.append(ugettext(res.get(key)))

                    elif key == 'error_msg':
                        error_msg = res.get(key)
                        if error_msg.find('| |') != -1:
                            error_msg = error_msg.split('| |,')[['en', 'fr'].index(language)]
                        submission.append(error_msg)
                    else:
                        submission.append(res.get(ugettext(key)))
            submissions.append(submission)
        return submissions
