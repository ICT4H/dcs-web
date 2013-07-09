from unittest import TestCase
import urllib2
from django.http import HttpRequest
import jsonpickle
from mock import Mock, patch
from mangrove.errors.MangroveException import FormModelDoesNotExistsException
from mangrove.datastore.database import DatabaseManager

http_basic_patch = patch('datawinners.feeds.authorization.httpbasic', lambda x: x)
http_basic_patch.start()
datasender_patch = patch('datawinners.feeds.authorization.is_not_datasender', lambda x: x)
datasender_patch.start()
from datawinners.feeds.views import feed_entries


class TestFeedView(TestCase):
    def test_error_when_form_code_is_not_present(self):
        request = HttpRequest()
        request.GET['start_date'] = urllib2.quote("21-12-2001 12:12:57".encode("utf-8"))
        request.GET['end_date'] = urllib2.quote("21-12-2002 12:12:57".encode("utf-8"))
        request.user = 'someuser'

        with patch('datawinners.feeds.views.get_form_model_by_code') as get_form_model_by_code:
            with patch('datawinners.feeds.views.get_database_manager') as get_db_manager:
                get_db_manager.return_value = Mock(spec=DatabaseManager)
                get_form_model_by_code.side_effect = FormModelDoesNotExistsException(None)
                response = feed_entries(request, None)
                self.assertEqual(400, response.status_code)
                response_content = jsonpickle.decode(response.content)
                self.assertEquals(response_content.get('ERROR_CODE'), 101)
                self.assertEquals(response_content.get('ERROR_MESSAGE'), 'Invalid form code provided')

    def test_error_when_form_code_is_empty(self):
        request = HttpRequest()
        request.GET['start_date'] = urllib2.quote("21-12-2001 12:12:57".encode("utf-8"))
        request.GET['end_date'] = urllib2.quote("21-12-2002 12:12:57".encode("utf-8"))
        request.user = 'someuser'
        with patch('datawinners.feeds.views.get_form_model_by_code') as get_form_model_by_code:
            with patch('datawinners.feeds.views.get_database_manager') as get_db_manager:
                get_db_manager.return_value = Mock(spec=DatabaseManager)
                get_form_model_by_code.side_effect = FormModelDoesNotExistsException('  ')
                response = feed_entries(request, "     ")
                self.assertEqual(400, response.status_code)
                response_content = jsonpickle.decode(response.content)
                self.assertEquals(response_content.get('ERROR_CODE'), 101)
                self.assertEquals(response_content.get('ERROR_MESSAGE'), 'Invalid form code provided')


    def test_error_when_form_code_invalid(self):
        request = HttpRequest()
        request.GET['start_date'] = urllib2.quote("21-12-2001 12:12:57".encode("utf-8"))
        request.GET['end_date'] = urllib2.quote("21-12-2002 12:12:57".encode("utf-8"))
        request.user = 'someuser'
        with patch('datawinners.feeds.views.get_form_model_by_code') as get_form_model_by_code:
            with patch('datawinners.feeds.views.get_database_manager') as get_db_manager:
                get_db_manager.return_value = Mock(spec=DatabaseManager)
                get_form_model_by_code.side_effect = FormModelDoesNotExistsException('non-existent-form-code')
                response = feed_entries(request, "non-existent-form-code")
                self.assertEqual(400, response.status_code)
                response_content = jsonpickle.decode(response.content)
                self.assertEquals(response_content.get('ERROR_CODE'), 101)
                self.assertEquals(response_content.get('ERROR_MESSAGE'), 'Invalid form code provided')


    def test_error_when_start_date_not_provided(self):
        request = HttpRequest()
        response = feed_entries(request, "cli001")
        self.assertEqual(400, response.status_code)
        response_content = jsonpickle.decode(response.content)
        self.assertEquals(response_content.get('ERROR_CODE'), 102)
        self.assertEquals(response_content.get('ERROR_MESSAGE'), 'Invalid Start Date provided')


    def test_error_when_start_date_is_empty(self):
        request = HttpRequest()
        request.GET['start_date'] = "     "

        response = feed_entries(request, "cli001")
        self.assertEqual(400, response.status_code)
        response_content = jsonpickle.decode(response.content)
        self.assertEquals(response_content.get('ERROR_CODE'), 102)
        self.assertEquals(response_content.get('ERROR_MESSAGE'), 'Invalid Start Date provided')


    def test_error_when_start_date_is_not_in_correct_format(self):
        request = HttpRequest()
        request.GET['start_date'] = urllib2.quote("21/12/2001".encode("utf-8"))
        response = feed_entries(request, "cli001")
        self.assertEqual(400, response.status_code)
        response_content = jsonpickle.decode(response.content)
        self.assertEquals(response_content.get('ERROR_CODE'), 102)
        self.assertEquals(response_content.get('ERROR_MESSAGE'), 'Invalid Start Date provided')

    def test_error_when_end_date_not_provided(self):
        request = HttpRequest()
        request.GET['start_date'] = urllib2.quote("21-12-2001 12:12:57".encode("utf-8"))
        response = feed_entries(request, "cli001")
        self.assertEqual(400, response.status_code)
        response_content = jsonpickle.decode(response.content)
        self.assertEquals(response_content.get('ERROR_CODE'), 102)
        self.assertEquals(response_content.get('ERROR_MESSAGE'), 'Invalid End Date provided')


    def test_error_when_end_date_is_empty(self):
        request = HttpRequest()
        request.GET['start_date'] = urllib2.quote("21-12-2001 12:12:57".encode("utf-8"))
        request.GET['end_date'] = "   "

        response = feed_entries(request, "cli001")
        self.assertEqual(400, response.status_code)
        response_content = jsonpickle.decode(response.content)
        self.assertEquals(response_content.get('ERROR_CODE'), 102)
        self.assertEquals(response_content.get('ERROR_MESSAGE'), 'Invalid End Date provided')


    def test_error_when_end_date_is_not_in_correct_format(self):
        request = HttpRequest()
        request.GET['start_date'] = urllib2.quote("21-12-2001 12:12:57".encode("utf-8"))
        request.GET['end_date'] = urllib2.quote("21-12-2001".encode("utf-8"))

        response = feed_entries(request, "cli001")
        self.assertEqual(400, response.status_code)
        response_content = jsonpickle.decode(response.content)
        self.assertEquals(response_content.get('ERROR_CODE'), 102)
        self.assertEquals(response_content.get('ERROR_MESSAGE'), 'Invalid End Date provided')

    def test_error_when_end_date_is_less_than_start_date(self):
        request = HttpRequest()
        request.GET['start_date'] = urllib2.quote("21-12-2001 12:12:57".encode("utf-8"))
        request.GET['end_date'] = urllib2.quote("21-12-2001 12:12:56".encode("utf-8"))

        response = feed_entries(request, "cli001")
        self.assertEqual(400, response.status_code)
        response_content = jsonpickle.decode(response.content)
        self.assertEquals(response_content.get('ERROR_CODE'), 103)
        self.assertEquals(response_content.get('ERROR_MESSAGE'), 'End Date provided is less than Start Date')


http_basic_patch.stop()
datasender_patch.stop()