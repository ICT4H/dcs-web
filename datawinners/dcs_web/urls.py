from django.conf.urls.defaults import patterns
from datawinners.accountmanagement.forms import MinimalRegistrationForm
from datawinners.dcs_web.view import terms_and_conditions, home

urlpatterns = patterns('',
                           (r'^registration/$', 'registration.views.register',
                        {'form_class': MinimalRegistrationForm, 'template_name': 'registration/registration.html',
                         'backend': 'datawinners.dcs_web.registration_backend.DCSRegistrationBackend'}),
                        (r'^en/terms-and-conditions/$', terms_and_conditions),
                        (r'^en/home/', home),

)