import os
import unittest
import time

from django.contrib.auth.models import User

from datawinners.blue.correlated_xlxform import CorrelatedForms, NoCommonFieldsException, MultipleChildrenNotSupported, \
    ParentProjectWithFieldSetNotSupported
from datawinners.blue.xform_bridge import XlsFormParser, MangroveService
from datawinners.main.database import get_database_manager
from mangrove.form_model.project import Project


DIR = os.path.dirname(__file__)

class TestCorrelatedXlsForms(unittest.TestCase):

    def setUp(self):
        self.test_data = os.path.join(DIR, 'testdata')
        self.REPAYMENT = os.path.join(self.test_data, 'repayment.xls')
        self.LOAN_ACCOUNT = os.path.join(self.test_data, 'loan-account.xls')
        self.NO_MATCHING_FIELDS = os.path.join(self.test_data, 'no-fields-matching-repayment.xls')
        self.REPEAT = os.path.join(self.test_data,'repeat.xls')
        self.user = User.objects.get(username="tester150411@gmail.com")
        self.dbm = get_database_manager(self.user)
        self.random_project_name = str(time.time())
        #Do this before creating projects for this test suite
        self.repayment_project_id = self._create_test_projects('Repayment-' + self.random_project_name, self.REPAYMENT)
        self.loan_account_id = self._create_test_projects('Loan account-'+ self.random_project_name, self.LOAN_ACCOUNT)

    def test_should_add_parent_info_to_child_questionnaire(self):
        correlated_forms = CorrelatedForms(self.user)

        correlated_forms.relate_forms(self.loan_account_id, self.repayment_project_id, 'Repayment')

        updated_child_project = Project.get(self.dbm, self.repayment_project_id)
        self._asset_parent_fields_code_label(updated_child_project)
        self.assertEqual(updated_child_project.parent_info.get("action_label"), 'Repayment')
        self.assertTrue(updated_child_project.is_child_project)

    def _asset_parent_fields_code_label(self, updated_child_project):
        self.assertEqual(updated_child_project.parent_info.get("parent_fields_code_label"),
                             {'loan_ac_number': 'Loan a/c number',
                              'borrower_id': 'Borrower ID',
                              'borrower_name': 'Borrower Name'})

    def test_should_verify_parent_and_child_project_has_at_least_one_common_field_to_establish_relation(self):
        correlated_forms = CorrelatedForms(self.user)
        project_with_no_matching_fields_with_loan_account = self._create_test_projects('no-matching-fields-'
                                                                               + self.random_project_name, self.NO_MATCHING_FIELDS)
        with self.assertRaises(NoCommonFieldsException):
            correlated_forms.relate_forms(self.loan_account_id, project_with_no_matching_fields_with_loan_account,
                                          'New Child')

    def test_should_add_child_id_to_parent_questionnaire(self):
        correlated_forms = CorrelatedForms(self.user)

        correlated_forms.relate_forms(self.loan_account_id, self.repayment_project_id, 'Repayment')

        updated_parent_project = Project.get(self.dbm, self.loan_account_id)
        self.assertIn(self.repayment_project_id, updated_parent_project.child_ids)
        self.assertTrue(updated_parent_project.is_parent_project)

    #TODO remove when multiple children support is build
    def test_should_not_allow_to_have_multiple_children(self):
        correlated_forms = CorrelatedForms(self.user)
        correlated_forms.relate_forms(self.loan_account_id, self.repayment_project_id, 'Repayment')

        with self.assertRaises(MultipleChildrenNotSupported):
            correlated_forms.relate_forms(self.loan_account_id, self.repayment_project_id, 'Repayment')

    def test_should_hide_common_parent_fields_in_child_xform_when_accessed_by_dcs_apis(self):
        # This needs to be done only for dcs app. For odk and web the parent fields remain editable.
        pass

    def test_should_not_allow_parent_to_contain_field_set_field_to_support_excel_import(self):
        project_with_repeat_field = self._create_test_projects('Project-with-repeat-'
                                                                               + self.random_project_name, self.REPEAT)
        correlated_forms = CorrelatedForms(self.user)
        with self.assertRaises(ParentProjectWithFieldSetNotSupported):
            correlated_forms.relate_forms(project_with_repeat_field, self.repayment_project_id, 'Repayment')



    def _create_test_projects(self, prj_name, xlxform):
        errors, xform, json_xform_data = XlsFormParser(xlxform, prj_name).parse()
        mangroveService = MangroveService(self.user, xform, json_xform_data, project_name=prj_name)
        project_id, form_code = mangroveService.create_project()
        return project_id
