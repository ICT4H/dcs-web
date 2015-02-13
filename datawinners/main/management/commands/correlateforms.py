from django.contrib.auth.models import User
from datawinners.blue.correlated_xlxform import CorrelatedForms
from django.core.management import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **options):

        if len(args) < 2:
            print "Please provide parent and child project uuids"
            return

        self.parent_uuid = args[0]
        self.child_uuid = args[1]
        user_name = args[2] if len(args) > 2 else 'tester150411@gmail.com'

        self.user = User.objects.get(username=user_name)
        self.new_child_action_label= 'Repayment'
        print "Trying to correlate parent: %s; child: %s" %(self.parent_uuid, self.child_uuid)
        self._correlate_projects()

    def _correlate_projects(self):
        correlated_forms = CorrelatedForms(self.user)
        if correlated_forms.relate_forms(self.parent_uuid, self.child_uuid, self.new_child_action_label):
            print('Project related successfully')
        else:
            print('Failed to relate project')
