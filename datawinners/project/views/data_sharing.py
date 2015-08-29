from datawinners.search.index_utils import es_questionnaire_field_name

DS_TAG_IS_EMPTY = 'ds_tag_is_empty'

class DataSharing():

    def __init__(self, form_model=None, user=None):
        self.form_model = form_model
        self.user = user

    def append_data_filter(self, search_filters):

        from_has_no_tag_field = not self.form_model.has_tag_field()
        current_user_is_admin = DataSharing().is_admin(self.user)

        if from_has_no_tag_field or current_user_is_admin:
            return


        es_ds_tag = es_questionnaire_field_name('tag', self.form_model.id) + '_exact'
        if self.user.get_profile().is_tag_assigned():
            search_filters.update({'tag': {es_ds_tag : self.user.get_profile().get_assigned_tag()}})
        else:
            # user tag is empty; match only empty tag records/data
            search_filters.update({DS_TAG_IS_EMPTY: {"field": es_ds_tag}})

    @classmethod
    def is_admin(cls, user):
        return user.groups.filter(name="NGO Admins").count() > 0
