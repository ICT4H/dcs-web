from sets import Set

from datawinners.main.database import get_database_manager
from mangrove.form_model.project import Project


class CorrelatedForms():

    def __init__(self, user):
        self.user = user
        self.dbm = get_database_manager(self.user)

    def _get_common_fields(self, parent_project, child_project):
        parent_field_codes = self._get_field_codes(parent_project)
        child_field_codes = self._get_field_codes(child_project)
        return parent_field_codes.intersection(child_field_codes)

    def relate_forms(self, parent_id, child_id, new_child_action_label_from_parent):
        parent_project = Project.get(self.dbm, parent_id)
        child_project = Project.get(self.dbm, child_id)
        common_fields = list(self._get_common_fields(parent_project, child_project))
        if parent_project.is_field_set_field_present():
            raise ParentProjectWithFieldSetNotSupported()
        if len(common_fields) == 0:
            raise NoCommonFieldsException()
        if parent_project.is_parent_project:
            raise MultipleChildrenNotSupported()

        code_label_dict = self._get_code_label_dict(parent_project, common_fields)
        child_project.set_parent_info(code_label_dict, new_child_action_label_from_parent)
        parent_project.add_child(child_id)
        parent_project.save(process_post_update=False)
        child_project.save(process_post_update=False)
        return True

    @staticmethod
    def _get_field_codes(project):
        return Set([field['code'] for field in project.form_fields if field.get('code')])

    @staticmethod
    def _get_code_label_dict(project, field_codes):
        return {field['code']:field['label'] for field in project.form_fields if field.get('code') in field_codes}

class ParentProjectWithFieldSetNotSupported(Exception):
    pass

class NoCommonFieldsException(Exception):
    pass

class MultipleChildrenNotSupported(Exception):
    pass
