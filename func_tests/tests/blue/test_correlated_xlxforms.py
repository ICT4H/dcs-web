from xml.etree import ElementTree as ET
import os
import unittest
import time

from django.contrib.auth.models import User

from datawinners.alldata.helper import get_all_project_for_user
from datawinners.blue.correlated_xlxform import CorrelatedForms, NoCommonFieldsException, ParentXform
from datawinners.blue.xform_bridge import XlsFormParser, MangroveService
from datawinners.main.database import get_database_manager
from datawinners.project import helper
from mangrove.form_model.project import Project


DIR = os.path.dirname(__file__)

class TestCorrelatedXlsForms(unittest.TestCase):

    def setUp(self):
        self.test_data = os.path.join(DIR, 'testdata')
        self.REPAYMENT = os.path.join(self.test_data, 'repayment.xls')
        self.LOAN_ACCOUNT = os.path.join(self.test_data, 'loan-account.xls')
        self.NO_MATCHING_FIELDS = os.path.join(self.test_data, 'no-fields-matching-repayment.xls')
        self.REPEAT = os.path.join(self.test_data,'repeat.xls')
        self.REPEAT_PARENT = os.path.join(self.test_data,'repeat-parent.xls')
        self.TWO_FIELDS_XFORM = os.path.join(self.test_data,'two-fields-xform.xml')
        self.user = User.objects.get(username="tester150411@gmail.com")
        self.dbm = get_database_manager(self.user)
        self.random_project_name = str(time.time())
        #Do this before creating projects for this test suite
        self.clean_projects = set()
        self.repayment_project_id = self._create_test_projects_and_delete_teardown('Repayment-' + self.random_project_name, self.REPAYMENT)
        self.loan_account_id = self._create_test_projects_and_delete_teardown('Loan account-'+ self.random_project_name, self.LOAN_ACCOUNT)

    def tearDown(self):
        self._delete_all_projects_created_by_this_test_run()

    def _delete_all_projects_created_by_this_test_run(self):
        questionnaires = get_all_project_for_user(self.user)
        ids = [q['value']['_id'] for q in questionnaires if q['value']['_id'] in self.clean_projects]
        [self._del_project(Project.get(self.dbm, id)) for id in ids]

    def _del_project(self, project):
        helper.delete_project(project)
        return project.delete()

    def test_should_add_parent_info_to_child_questionnaire(self):
        correlated_forms = CorrelatedForms(self.user)

        correlated_forms.relate_parent_and_child_forms(self.loan_account_id, self.repayment_project_id, 'Repayment')

        updated_child_project = Project.get(self.dbm, self.repayment_project_id)
        self._asset_parent_fields_code_label(updated_child_project)
        self.assertEqual(updated_child_project.parent_info.get("parent_uuid"), self.loan_account_id)
        self.assertEqual(updated_child_project.parent_info.get("action_label"), 'Repayment')
        self.assertTrue(updated_child_project.is_child_project)

    def _asset_parent_fields_code_label(self, updated_child_project):
        self.assertEqual(updated_child_project.parent_info.get("parent_fields_code_label"),
                             {'loan_ac_number': 'Loan a/c number',
                              'borrower_id': 'Borrower ID',
                              'borrower_name': 'Borrower Name'})

    def test_should_verify_parent_and_child_project_has_at_least_one_common_field_to_establish_relation(self):
        correlated_forms = CorrelatedForms(self.user)
        project_with_no_matching_fields_with_loan_account = self._create_test_projects_and_delete_teardown('no-matching-fields-'
                                                                               + self.random_project_name, self.NO_MATCHING_FIELDS)
        with self.assertRaises(NoCommonFieldsException):
            correlated_forms.relate_parent_and_child_forms(self.loan_account_id, project_with_no_matching_fields_with_loan_account,
                                          'New Child')

    def test_should_add_child_id_to_parent_questionnaire(self):
        correlated_forms = CorrelatedForms(self.user)

        correlated_forms.relate_parent_and_child_forms(self.loan_account_id, self.repayment_project_id, 'Repayment')

        updated_parent_project = Project.get(self.dbm, self.loan_account_id)
        self.assertIn(self.repayment_project_id, updated_parent_project.child_ids)
        self.assertTrue(updated_parent_project.is_parent_project)

    def test_should_verify_child_has_only_the_recent_parent_and_old_parent_do_not_have_child(self):
        correlated_forms = CorrelatedForms(self.user)
        correlated_forms.relate_parent_and_child_forms(self.loan_account_id, self.repayment_project_id, 'Repayment')
        new_loan_form_id = self._create_test_projects_and_delete_teardown('New Loan account-'+ self.random_project_name, self.LOAN_ACCOUNT)

        correlated_forms.relate_parent_and_child_forms(new_loan_form_id, self.repayment_project_id, 'Repayment')

        updated_child_project = Project.get(self.dbm, self.repayment_project_id)
        self.assertEqual(updated_child_project.parent_info.get("parent_uuid"), new_loan_form_id)

        prev_parent_project = Project.get(self.dbm, self.loan_account_id)
        self.assertNotIn(self.repayment_project_id, prev_parent_project.child_ids)

    def test_should_hide_common_parent_fields_in_child_xform_when_accessed_by_dcs_apis(self):
        # This needs to be done only for dcs app. For odk and web the parent fields remain editable.
        pass

    def test_should_relate_child_containing_field_set_question(self):
        correlated_forms = CorrelatedForms(self.user)
        project_with_repeat_field = self._create_test_projects_and_delete_teardown('Project-with-repeat-'
                                                                               + self.random_project_name, self.REPEAT)
        project_repeat_parent = self._create_test_projects_and_delete_teardown('Project-repeat-parent'
                                                                               + self.random_project_name, self.REPEAT_PARENT)
        correlated_forms.relate_parent_and_child_forms(project_repeat_parent, project_with_repeat_field, 'Child-with-repeat')

        updated_child_project = Project.get(self.dbm, project_with_repeat_field)

        self.assertEqual(updated_child_project.parent_info.get("parent_fields_code_label"),
                                                                {'familyname': 'What is the family name?'})
        self.assertEqual(updated_child_project.parent_info.get("action_label"), 'Child-with-repeat')
        self.assertTrue(updated_child_project.is_child_project)

    def test_parent_project_fields_are_read_only(self):
        xform_as_string = open(self.TWO_FIELDS_XFORM, 'r').read()

        output = ParentXform().make_all_fields_read_only(xform_as_string)

        bind_tag = '{http://www.w3.org/1999/xhtml}head/{http://www.w3.org/2002/xforms}model/{http://www.w3.org/2002/xforms}bind'
        self._assert_readonly_is_true(output, bind_tag)

    def _assert_readonly_is_true(self, source_xml_str, bind_tag):
        root = ET.fromstring(source_xml_str.encode('utf-8'))
        [self.assertTrue('true()', r.attrib['readonly']) for r in root.iterfind(bind_tag)]

    def _create_test_projects_and_delete_teardown(self, prj_name, xlxform):
        errors, xform, json_xform_data = XlsFormParser(xlxform, prj_name).parse()
        mangroveService = MangroveService(self.user, xform, json_xform_data, project_name=prj_name)
        project_id, form_code = mangroveService.create_project()
        self.clean_projects.add(project_id)
        return project_id
