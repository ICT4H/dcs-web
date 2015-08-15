from datawinners.search.index_utils import es_questionnaire_field_name


class DataSharing():

    def __init__(self, form_model=None, user=None):
        self.form_model = form_model
        self.user = user

    def append_data_filter(self, search_filters):

        if not self.form_model.has_tag_field() or DataSharing().is_admin(self.user):
            return

        es_ds_tag = es_questionnaire_field_name('tag', self.form_model.id) + '_exact'
        if self.user.get_profile().is_tag_assigned():
            search_filters.update({'tag': {es_ds_tag : self.user.get_profile().get_assigned_tag()}})
        else:
            EMPTY_TAG = ''
            search_filters.update({'tag': {es_ds_tag : EMPTY_TAG}})

    @classmethod
    def is_admin(cls, user):
        return user.groups.filter(name="NGO Admins").count() > 0
