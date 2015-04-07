import os
import unittest
import time

from django.contrib.auth.models import User

from datawinners.alldata.helper import get_all_project_for_user
from datawinners.blue.view import set_mobile_displayable_fields
from datawinners.blue.xform_bridge import MangroveService, XlsFormParser
from datawinners.main.database import get_database_manager
from mangrove.form_model.project import Project
from datawinners.project import helper


DIR = os.path.dirname(__file__)

class TestAssociateHeaderToQuestionnaire(unittest.TestCase):
    def setUp(self):
        self.test_data = os.path.join(DIR, 'testdata')
        self.questionnaire = os.path.join(self.test_data, 'text_and_integer.xls')
        self.user = User.objects.get(username="tester150411@gmail.com")
        self.dbm = get_database_manager(self.user)
        self.clean_projects = set()
        self.random_project_name = str(time.time())
        self.simple_project_id = self._create_test_projects_and_delete_teardown('Simple-' + self.random_project_name, self.questionnaire)

    def tearDown(self):
        self._delete_all_projects_created_by_this_test_run()

    def _delete_all_projects_created_by_this_test_run(self):
        questionnaires = get_all_project_for_user(self.user)
        ids = [q['value']['_id'] for q in questionnaires if q['value']['_id'] in self.clean_projects]
        [self._del_project(Project.get(self.dbm, id)) for id in ids]

    def _del_project(self, project):
        helper.delete_project(project)
        return project.delete()

    def _create_test_projects_and_delete_teardown(self, prj_name, xlxform):
        errors, xform, json_xform_data = XlsFormParser(xlxform, prj_name).parse()
        mangroveService = MangroveService(self.user, xform, json_xform_data, project_name=prj_name)
        project_id, form_code = mangroveService.create_project()
        self.clean_projects.add(project_id)
        return project_id

    def test_should_add_header_to_project(self):
        selected_field_codes = ["your_name", "your_age"]
        expected_mobile_main_header = [{"name":'your_name', "label": "What is your name?"},
                                       {"name":"your_age", "label": "How many years old are you?"}]

        set_mobile_displayable_fields(self.user, self.simple_project_id, selected_field_codes)

        simple_project = Project.get(self.dbm, self.simple_project_id)
        self.assertEquals(simple_project.mobile_main_fields, expected_mobile_main_header)