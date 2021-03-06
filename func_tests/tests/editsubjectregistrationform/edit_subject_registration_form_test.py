from framework.base_test import BaseTest, HeadlessRunnerTest
from framework.utils.common_utils import generateId
from pages.addsubjecttypepage.add_subject_type_page import AddSubjectTypePage
from pages.loginpage.login_page import LoginPage, login
from pages.projectsubjectspage.project_subjects_page import ProjectSubjectsPage
from testdata.test_data import DATA_WINNER_LOGIN_PAGE, url
from tests.subjecttypetests.add_subject_type_data import VALID_ENTITY, ENTITY_TYPE
from tests.logintests.login_data import VALID_CREDENTIALS
from nose.plugins.attrib import attr

class TestEditSubjectRegistrationForm(HeadlessRunnerTest):

    @attr('functional_test')
    def test_should_add_question_successfully(self):
        login(self.driver, VALID_CREDENTIALS)
        self.driver.go_to(url("/entity/subjects/"))
        add_subject_type_page = AddSubjectTypePage(self.driver)
        add_subject_type_page.click_on_accordian_link()
        entity_type = VALID_ENTITY[ENTITY_TYPE] + generateId()
        add_subject_type_page.successfully_add_entity_type_with(entity_type)
        self.driver.go_to(url("/entity/subject/create/" + entity_type))
        subjects_page = ProjectSubjectsPage(self.driver)
        subjects_page.click_edit_form_link_and_continue()
        subjects_page.click_add_question_link()
        subjects_page.type_question_name('New Question')
        subjects_page.choose_question_type('text')
        self.assertEqual("New Question", subjects_page.get_selected_question_label())

        existing_question_count = subjects_page.get_existing_questions_count()

        subjects_page.click_submit_button()
        self.assertTrue(subjects_page.is_success_message_tip_show())
        subjects_page.refresh()
        self.assertEqual(subjects_page.get_existing_questions_count(), existing_question_count, "Newly added question should be persisted")

