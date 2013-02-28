from datawinners.project.Header import SubmissionsPageHeader
from main.utils import timebox
from project.data_sender import DataSender
from project.export_to_excel import format_field_values_for_excel
from submission_data import SubmissionData

class SubmissionListForExcel(SubmissionData):
    def __init__(self, form_model, manager, org_id, submission_type, filters, keyword=None):
        super(SubmissionListForExcel, self).__init__(form_model, manager, org_id, SubmissionsPageHeader,
            submission_type, filters, keyword)

    def get_leading_part(self):
        leading_part = []
        for submission in self.filtered_submissions:
            data_sender_tuple, rp, subject_tuple, submission_date = super(SubmissionListForExcel,
                self).get_submission_details_for_excel(submission)
            status = self._get_translated_submission_status(submission.status)
            error_message = submission.errors if submission.errors else "-"
            subject_id = subject_tuple[1] if subject_tuple else ""
            subject_name = subject_tuple[0] if subject_tuple else ""
            data_sender = DataSender.from_tuple(data_sender_tuple)
            leading_part.append(
                filter(lambda x: x, [submission.id, data_sender.name, data_sender.reporter_id, submission_date, status,
                                     error_message, subject_name, subject_id, rp]))
        return leading_part

    @timebox
    def _get_field_values(self):
        submission_values = [(submission.form_model_revision, submission.values) for submission in
                             self.filtered_submissions]
        field_values = []
        for row in submission_values:
            fields_ = []
            formatted_row = format_field_values_for_excel(row, self.form_model)
            for field in self.form_model.non_rp_fields_by():
                fields_.extend(self.order_formatted_row(field.code, formatted_row))
            field_values.append(fields_)
        return field_values
