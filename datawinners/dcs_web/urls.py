from django.conf.urls.defaults import patterns, include
from django.views.generic.simple import direct_to_template
from datawinners.accountmanagement.forms import MinimalRegistrationForm
import datawinners.settings as settings

urlpatterns = patterns('',

    (r'^media/homepage/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_HOME_PAGE}),

    (r'', include('datawinners.urls')), #including the datawinners url
    (r'', include('datawinners.dcs_app.urls')),

    (r'^en/terms-and-conditions/$', direct_to_template, {'template': 'terms_conditions.html'}),

    (r'^registration/$', 'registration.views.register',
    {'form_class': MinimalRegistrationForm, 'template_name': 'registration/registration.html',
     'backend': 'datawinners.dcs_web.registration_backend.DCSRegistrationBackend'})


)