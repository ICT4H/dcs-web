from sets import Set
from xml.etree import ElementTree as ET

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

    def _remove_child_and_save_parent(self, parent_project, child_id):
        parent_project.remove_child(child_id);
        parent_project.save()

    def _remove_child_from_parent(self, project_ids, child_id):
        if project_ids:
            [self._remove_child_and_save_parent(Project.get(self.dbm, p), child_id) for p in project_ids]

    def relate_parent_and_child_forms(self, parent_id, child_id, new_child_action_label_from_parent):
        child_project = Project.get(self.dbm, child_id)
        self._remove_child_from_parent(child_project.parent_uuids, child_id)
        #TODO write test to verify that parent is reloaded to avoid ResourceConflict('Document update conflict.',)
        parent_project = Project.get(self.dbm, parent_id)
        common_fields = list(self._get_common_fields(parent_project, child_project))
        if len(common_fields) == 0:
            raise NoCommonFieldsException()

        code_label_dict = self._get_code_label_dict(parent_project, common_fields)
        child_project.set_parent_info(parent_id, code_label_dict, new_child_action_label_from_parent)
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

class NoCommonFieldsException(Exception):
    pass


class ParentXform():

    def make_all_fields_read_only(self, xform_xml):
        ET.register_namespace('', 'http://www.w3.org/2002/xforms')

        root = ET.fromstring(xform_xml.encode('utf-8'))
        bind_element = '{http://www.w3.org/1999/xhtml}head/{http://www.w3.org/2002/xforms}model/{http://www.w3.org/2002/xforms}bind'
        [self._make_field_read_only(el) for el in root.iterfind(bind_element)]
        return '<?xml version="1.0"?>%s' % ET.tostring(root)

    def _make_field_read_only(self, el):
        el.set('readonly', 'true()')
