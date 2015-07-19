#!/bin/bash

curl -X DELETE http://localhost:9200/_all/

dropdb ftdb || echo 'ftdb is not present'

createdb -T template_postgis ftdb
#. /home/jenkins/virtual_env/datawinners/bin/activate

WORKSPACE='/home/yogeshsr/workspace/datawinners'
cd $WORKSPACE
#git submodule update --init
#ps -ef|grep 'Xvfb :99' |grep -v grep || Xvfb :99 -ac >>/dev/null 2>&1 &
#export DISPLAY=":99"
export PYTHONPATH=$WORKSPACE/func_tests
export LANG=en_US.UTF-8

#pip install -r requirements.pip --download-cache=~/.pip-download-cache/
#deactivate
#. /home/jenkins/virtual_env/datawinners/bin/activate

#Yogi temp done
#pip install pyscss==1.3.2

cp datawinners/config/local_settings_ft.py datawinners/local_settings.py
cp datawinners/config/local_settings_ft.py func_tests/resources/local_settings.py


cd datawinners
#export PATH=/home/jenkins/bin:$PATH
export PYTHONPATH=$WORKSPACE
python manage.py syncdb --noinput
python manage.py migrate --noinput
python manage.py recreatedb
python manage.py recreatefeeddb
export PYTHONPATH=$WORKSPACE/func_tests
python manage.py recreate_search_indexes
python manage.py compilemessages
python manage.py compile_css


#gunicorn_django -D -b 0.0.0.0:9000 --pid=/tmp/mangrove_gunicorn_${JOB_NAME}

# Remove old screenshots
#rm -rf $WORKSPACE/func_tests/screenshots

cd $WORKSPACE/func_tests  && nosetests -v -A "functional_test" --with-xunit --xunit-file=${WORKSPACE}/xunit.xml --process-timeout=900

export PYTHONPATH=$WORKSPACE/integration_tests
cd $WORKSPACE/integration_tests  && nosetests -v -A "integration_test" --with-xunit --xunit-file=${WORKSPACE}/xunit-integration.xml --process-timeout=900

cd ..

#SUCCESS_TAG=${GIT_BRANCH##[[:alpha:]]*/}-ft-ok
#git tag -f -a -m "Functional tests ok" $SUCCESS_TAG && git push origin $SUCCESS_TAG

#kill `cat /tmp/mangrove_gunicorn_${JOB_NAME}`


