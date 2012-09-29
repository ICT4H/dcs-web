#encoding=utf-8
from collections import OrderedDict
from mangrove.datastore.entity import get_by_short_code
from mangrove.errors.MangroveException import DataObjectNotFound
from mangrove.form_model.field import SelectField
from mangrove.form_model.form_model import FormModel
from project import helper
from project.filters import KeywordFilter
from project.helper import filter_submissions, get_data_sender, _to_str, case_insensitive_lookup, NOT_AVAILABLE
from enhancer import form_model_enhancer, field_enhancer
from utils import sorted_unique_list

NULL = '--'
field_enhancer.enhance()
form_model_enhancer.enhance()

class SubmissionAnalyzer(object):
    def __init__(self, form_model, manager, request, filters, keyword=None):
        assert isinstance(form_model, FormModel)
        self.form_model = form_model
        self.manager = manager
        self.request = request
        self.filtered_submissions = filter_submissions(filters, self.form_model, self.manager)
        self._data_senders = []
        self._subject_list = []
        self.keyword_filter = KeywordFilter(keyword if keyword else '')
        self.leading_part_length = 0
        self.filtered_leading_part = []
        self._init_raw_values()

    def get_raw_values(self):
        return self._raw_values

    def get_headers(self):
        return helper.get_headers(self.form_model)

    def get_subjects(self):
        if self.form_model.entity_defaults_to_reporter():  return []
        subjects =  [row[0] for row in self.filtered_leading_part if row[0][1] != NULL]
        return sorted(list(set(subjects)))

    def get_data_senders(self):
        return sorted_unique_list(each[-1] for each in self.filtered_leading_part)

    def get_analysis_statistics(self):
        if not self._raw_values: return []

        field_header = self.get_headers()[self.leading_part_length:]
        result = self._init_statistics_result()
        for row in self._raw_values:
            for idx, question_values in enumerate(row[self.leading_part_length:]):
                question_name = field_header[idx]
                if isinstance(self.form_model.get_field_by_name(question_name), SelectField) and question_values:
                    result[question_name]['total'] += 1
                    for each in question_values:
                        result[question_name]['choices'][each] += 1

        list_result = []
        for key,value in result.items():
            row = [key, value['type'], value['total'], []]
            sorted_value = sorted(value['choices'].items(), key=lambda t:(t[1]*-1,t[0]))
            for option, count in sorted_value:
                row[-1].append([option,count])
            list_result.append(row)
        return list_result

    def _init_raw_values(self):
        field_values = self._get_field_values()
        leading_part = self._get_leading_part()
        raw_field_values = [leading + remaining[1:] for leading, remaining in zip(leading_part, field_values)]
        self._raw_values = self.keyword_filter.filter(raw_field_values)
        if leading_part:
            self.leading_part_length = len(leading_part[0])
            self.filtered_leading_part = [raw_value_row[:self.leading_part_length] for raw_value_row in self._raw_values]

    def _get_leading_part(self):
        leading_part = []
        for submission in self.filtered_submissions:
            data_sender = self._get_data_sender(submission)
            submission_date = _to_str(submission.created)
            row = [submission_date, data_sender]
            row = self._update_leading_part_for_rp(row, submission)
            row = self._update_leading_part_for_project_type(row, submission)
            leading_part.append(row)

        return leading_part

    def _get_field_values(self):
        submission_values = [submission.values for submission in self.filtered_submissions]
        field_values = []
        for row in submission_values:
            self._replace_option_with_real_answer_value(row)
            fields_ = [case_insensitive_lookup(field.code, row) for field in self.form_model.non_rp_fields()]
            field_values.append(fields_)
        return field_values

    def _get_data_sender(self, submission):
        for each in self._data_senders:
            if each[-1] == submission.source:
                return each
        else:
            data_sender = get_data_sender(self.manager, self.request.user, submission)
            self._data_senders.append(data_sender)
            return data_sender

    def _get_subject(self, submission):
        subject_code = case_insensitive_lookup(self.form_model.entity_question.code, submission.values)
        for each in self._subject_list:
            if each[-1] == subject_code:
                return each
        else:
            try:
                entity = get_by_short_code(self.manager, subject_code, [self.form_model.entity_type[0]])
                subject = entity.data['name']['value'], entity.short_code
            except DataObjectNotFound:
                subject =  NOT_AVAILABLE, subject_code

            self._subject_list.append(subject)
            return subject

    def _update_leading_part_for_rp(self, row, submission):
        rp_field = self.form_model.event_time_question
        if rp_field:
            reporting_period = case_insensitive_lookup(rp_field.code, submission.values)
            reporting_period = _to_str(reporting_period, rp_field)
            return [reporting_period] + row
        else:
            return row

    def _update_leading_part_for_project_type(self, row, submission):
        if  self.form_model.entity_defaults_to_reporter(): return row
        subject = self._get_subject(submission)
        return [subject] + row

    def _replace_option_with_real_answer_value(self, row):
        assert isinstance(row, dict)
        for question_code,question_value in row.iteritems():
            field = self.form_model.get_field_by_code(question_code)
            if isinstance(field,SelectField):
                row[question_code] = field.get_option_value_list(question_value)

    def _init_statistics_result(self):
        result = OrderedDict()
        for each in self.form_model.fields:
            if isinstance(each, SelectField):
                result.setdefault(each.name, {"choices":{},"type":each.type,'total':0})
                for option in each.options:
                    result[each.name]['choices'][option['text'][each.language]] = 0
        return result


def get_formatted_values_for_list(values):
    formatted_values = []
    for row in values:
        result = _format_row(row)
        formatted_values.append(list(result))
    return formatted_values

def _format_row(row):
    for each in row:
        if isinstance(each, tuple):
            new_val = '%s<span class="small_grey">%s</span>' % (each[0], each[1]) if each[1] else each[0]
        elif isinstance(each, list):
            new_val = ', '.join(each)
        elif each:
            new_val = each
        else:
            new_val = NULL
        yield new_val
