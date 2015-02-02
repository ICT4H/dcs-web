from django.contrib.auth.models import User
from django.core.management import BaseCommand

from datawinners.alldata.helper import get_all_project_for_user
from datawinners.main.database import get_database_manager
from datawinners.project import helper
from mangrove.form_model.project import Project


class Command(BaseCommand):
    def handle(self, *args, **options):

        user_name = 'tester150411@gmail.com'
        self.user = User.objects.get(username=user_name)
        self.dbm = get_database_manager(self.user)

        self.retain_project_ids = []

        if len(args) > 0 and 'all' == args[0]:
            self.retain_project_ids = args[1:] if len(args) > 1 else []
            print 'projects going to be retained: %s'% str(self.retain_project_ids)
            self._delete_all_projects_except()
        else:
            self._print_project_id_name()

    def _print_project_id_name(self):
        questionnaires = get_all_project_for_user(self.user)
        print 'Existing project:'
        print '\n'.join([q['value']['_id'] + ' --' +  q['value']['name'] for q in questionnaires])
        print '\n Pass all as option to delete all projects. Optionally followed with space separated project ids to be retained'

    def _delete_all_projects_except(self):
        questionnaires = get_all_project_for_user(self.user)
        ids = [q['value']['_id'] for q in questionnaires if q['value']['_id'] not in self.retain_project_ids]
        [self._del_project(Project.get(self.dbm, id)) for id in ids]

    def _del_project(self, project):
        helper.delete_project(project)
        return project.delete()