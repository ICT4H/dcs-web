from django.contrib.auth.models import User
from datawinners.blue.correlated_xlxform import CorrelatedForms
from django.core.management import BaseCommand
from datawinners.blue.view import set_mobile_displayable_fields


class Command(BaseCommand):

    def handle(self, *args, **options):

        if len(args) < 1:
            print "Please provide project_id"
            return

        self.project_uuid = args[0]
        self.headers = args[1].split(",") if len(args) > 1 else []
        user_name = args[2] if len(args) > 2 else 'tester150411@gmail.com'

        self.user = User.objects.get(username=user_name)

        print "Trying to add fields to : %s;" %(self.project_uuid)
        fields_stored = set_mobile_displayable_fields(self.user, self.project_uuid, self.headers)
        print " SuccessFully added fields to : %s" %(self.project_uuid)
        print fields_stored