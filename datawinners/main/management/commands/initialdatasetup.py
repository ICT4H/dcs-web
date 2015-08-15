# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from django.core.management.base import BaseCommand

from datawinners.main.couchdb.utils import all_db_names
from datawinners.main.database import get_db_manager
from mangrove.datastore.cache_manager import get_cache_manager
from mangrove.datastore.database import _delete_db_and_remove_db_manager
from mangrove.bootstrap import initializer as mangrove_intializer


class Command(BaseCommand):
    def handle(self, *args, **options):
        get_cache_manager().flush_all()
        for database_name in all_db_names():
            print ("Database %s") % (database_name,)
            print 'Creating initial data'
            manager = get_db_manager(database_name)
            mangrove_intializer.run(manager)

        print "Done."
