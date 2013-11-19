from collections import OrderedDict
import elasticutils
from datawinners.settings import ELASTIC_SEARCH_URL
from mangrove.form_model.form_model import header_fields
from datawinners.search.query import QueryBuilder, Query


class SubmissionQueryBuilder(QueryBuilder):
    def create_query(self, doc_type, database_name):
        return elasticutils.S().es(urls=ELASTIC_SEARCH_URL).indexes(database_name).doctypes(doc_type)

    def create_paginated_query(self, query, query_params):
        query = super(SubmissionQueryBuilder, self).create_paginated_query(query,query_params)
        submission_type_filter = query_params.get('filter')
        if submission_type_filter:
            if submission_type_filter == 'deleted':
                return query.filter(void=True)
            query = (query.filter(status=submission_type_filter))
        return query.filter(void=False)


class SubmissionQueryResponseCreator():
    def __init__(self, form_model):
        self.form_model = form_model

    def create_response(self, required_field_names, query):
        submissions = []
        for res in query.values_dict(tuple(required_field_names)):
            submission = []
            submission.append(res._id)
            submission.append([res.get('ds_name') + "<span class='small_grey'>  %s</span>" % res.get('ds_id')])

            for key in required_field_names:
                meta_fields = ['ds_id', 'ds_name', 'entity_short_code']
                if not key in meta_fields:
                    if key.lower() == self.form_model.entity_question.code.lower():
                        submission.append(
                            [res.get(key) + "<span class='small_grey'>  %s</span>" % res.get('entity_short_code')])
                    elif isinstance(res.get(key), dict):
                        submission.append(res.get(key).values())
                    else:
                        submission.append(res.get(key))
            submissions.append(submission)
        return submissions


class SubmissionQuery(Query):
    def __init__(self, form_model, query_params):
        Query.__init__(self, SubmissionQueryResponseCreator(form_model), SubmissionQueryBuilder(), query_params)
        self.form_model = form_model

    def get_headers(self, user, form_code):
        header_dict = OrderedDict()
        self._update_static_header_info(header_dict)

        def key_attribute(field): return self._field_code_in_lowercase(field)

        header_fields(self.form_model, key_attribute, header_dict)
        if "reporter" in self.form_model.entity_type:
            header_dict.pop(self.form_model.entity_question.code)
        return header_dict.keys()

    def _update_static_header_info(self, header_dict):
        header_dict.update({"ds_id": "Datasender Id"})
        header_dict.update({"ds_name": "Datasender Name"})
        header_dict.update({"date": "Submission Date"})
        submission_type = self.query_params.get('filter')
        if not submission_type  or submission_type == 'deleted':
            header_dict.update({"status": "Status"})
        elif submission_type == 'error': \
            header_dict.update({"error_msg": "Error Message"})
        header_dict.update({self._field_code_in_lowercase(self.form_model.entity_question): "Entity"})
        header_dict.update({'entity_short_code': "Entity short code"})
        if self.form_model.event_time_question:
            header_dict.update({self._field_code_in_lowercase(self.form_model.event_time_question): "Reporting Date"})

    def _field_code_in_lowercase(self, field):
        return field.code.lower()


    def populate_query_options(self):
        options = super(SubmissionQuery, self).populate_query_options()
        try:
            options.update({'filter': self.query_params["filter"]})
        except KeyError:
            pass
        return options
