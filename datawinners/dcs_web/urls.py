from django.conf.urls.defaults import patterns, include
from django.views.generic.simple import direct_to_template
from datawinners.accountmanagement.forms import MinimalRegistrationForm
import datawinners.settings as settings

urlpatterns = patterns('',

    (r'^media/CACHE/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_CACHE}),

    (r'^media/css/bootstrap/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_BOOTSTRAP}),
    (r'^media/css/font/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_FONT}),
    (r'^media/css/plugins/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_PLUGINS}),

    (r'^media/admin/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ADMIN}),
    (r'^media/files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_FILES}),
    (r'^media/images/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_IMAGES}),
    (r'^media/javascript/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_JS}),

    (r'^media/homepage/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_HOME_PAGE}),

    (r'', include('datawinners.urls')), #including the datawinners url
    (r'', include('datawinners.dcs_app.urls')),

    (r'^en/terms-and-conditions/$', direct_to_template, {'template': 'terms_conditions.html'}),

    (r'^registration/$', 'registration.views.register',
    {'form_class': MinimalRegistrationForm, 'template_name': 'registration/registration.html',
     'backend': 'datawinners.dcs_web.registration_backend.DCSRegistrationBackend'})


)