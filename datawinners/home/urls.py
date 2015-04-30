# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8
from datawinners.accountmanagement.forms import LoginForm
from datawinners.accountmanagement.views import custom_login
from django.conf.urls.defaults import patterns, url
from datawinners.home.views import index, switch_language, ask_us, blog, custom_home, open_skype

urlpatterns = patterns('',
        (r'^home/$', index),
        (r'^switch/(?P<language>.{2}?)/$', switch_language),
        (r'^home/ask-us/', ask_us),
        (r'^fr/about-us/blog/$', blog, {'language': 'fr'}),
        (r'^en/about-us/blog/$', blog, {'language': 'en'}),
        url(r'^$', custom_login, {'template_name': 'registration/login.html', 'authentication_form': LoginForm}, name='auth_login'),
        url(r'^$', custom_home),
        url(r'^openskype/', open_skype, name='open_skype'),
)