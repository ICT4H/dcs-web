#!/bin/bash

function migrate_db {
	echo "go migrate database"
	python "$DWROOT_DIR/datawinners/manage.py" migrate
}

function restore_couchdb_and_postgres {
  	check_host_is_dev && \
  	restore_postgresql_database && \
  	recreate_couch_db && \
  	recreate_feed_db && \
  	recreate_search_index
}

function unit_test {
	echo "running unit test"
	#compile_messages && \
	(cd "$DWROOT_DIR/datawinners" && python manage.py test --verbosity=2 --with-xunit --xunit-file=/tmp/nosetests.xml)
}

function mangrove_unit_test {
	echo "running mangrove unit test"
	(cd ~/virtual_env/datawinners/src/mangrove/mangrove && nosetests -v)
}

function js_tests {
    echo "running javascript unit tests"
    (cd "$DWROOT_DIR/datawinners/tests/js_test" && ./phantomjs.runner.sh ./jasmine_runner/*.html)
}

function recreate_couch_db {
    check_host_is_dev && \
	(cd "$DWROOT_DIR/datawinners" && python manage.py recreatedb)
}

function recreate_feed_db {
    check_host_is_dev && \
	(cd "$DWROOT_DIR/datawinners" && python manage.py recreatefeeddb)
}

function kill_gunicorn {
    if [ -f /tmp/mangrove_gunicorn_${JOB_NAME} ]
    then
        kill -9 `cat /tmp/mangrove_gunicorn_${JOB_NAME}`
    fi
}

function function_test {
	echo "running function test"
	export WORKSPACE=~/workspace/datawinners
    cd $WORKSPACE
    export PYTHONPATH=$WORKSPACE:$WORKSPACE/func_tests
    dropdb ftdb || echo ftdb database is not present
	createdb -T template_postgis ftdb
	#ps -ef|grep Xvfb |grep -v grep || Xvfb :99 -ac >>/dev/null 2>&1 &
    #export DISPLAY=":99"
    #export PYTHONPATH=$WORKSPACE
#    pip install -r requirements.pip
    cp datawinners/config/local_settings_ft.py datawinners/local_settings.py
    cp datawinners/config/local_settings_ft.py func_tests/resources/local_settings.py

	cd datawinners
    python manage.py syncdb --noinput
    python manage.py migrate --noinput
    python manage.py recreatedb
    python manage.py compilemessages
    kill_gunicorn
    gunicorn_django -D -b 0.0.0.0:9000 --pid=/tmp/mangrove_gunicorn_${JOB_NAME} -w 8
    cd $WORKSPACE/func_tests  && nosetests -v -a "functional_test" --with-xunit --xunit-file=${WORKSPACE}/xunit.xml --processes=1 --process-timeout=900
    kill_gunicorn

}

function smoke_test {
	echo "running smoke test"
	cp "$DWROOT_DIR/datawinners/config/local_settings_example.py" "$DWROOT_DIR/func_tests/resources/local_settings.py"
	(cd "$DWROOT_DIR/func_tests" && nosetests --rednose -v -a smoke)
}

function restore_postgresql_database {
	check_host_is_dev && \
	echo "recreating database"
	dropdb mangrove && createdb -T template_postgis mangrove && \
	(cd "$DWROOT_DIR/datawinners" && python manage.py syncdb --noinput && python manage.py migrate)
}

function compile_messages {
    cd "$DWROOT_DIR/datawinners" && python manage.py compilemessages
}

function check_host_is_dev {
    if [[ "$HOSTNAME" = *dwdev* ]]
    then
      return 0
    else
      return 1
    fi
}

function recreate_search_index {
  cd "$DWROOT_DIR/datawinners" && python manage.py recreate_search_indexes
}