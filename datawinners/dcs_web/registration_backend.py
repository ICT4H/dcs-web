from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from datawinners import settings
from registration.models import RegistrationProfile
from datawinners.accountmanagement.models import Organization
from datawinners.accountmanagement.registration_backend import RegistrationBackend


class DCSRegistrationBackend(RegistrationBackend):

    def create_respective_organization(self, kwargs):

        organization = Organization.create_trial_organization(kwargs)
        organization.account_type = 'Pro'
        return organization

    def get_registration_processor(self, organization):
        return DCSAccountRegistrationProcessor(organization)

class DCSAccountRegistrationProcessor(object):
    def __init__(self, organization):
        self.organization = organization
        self.template = 'pro_activation_email'

    def process(self, user, site, language, kwargs):
        self._send_activation_email(site, user, language)

    def _send_activation_email(self, site, user, language):
        ctx_dict = {'activation_key': RegistrationProfile.objects.get(user=user).activation_key,
                    'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                    'site': site,
                    'username': user.first_name}
        subject = render_to_string('registration/activation_email_subject_in_'+language+'.txt')
        subject = ''.join(subject.splitlines()) # Email subject *must not* contain newlines
        message = render_to_string('registration/' + self.template + '_in_'+language+'.html',
                                   ctx_dict)
        email = EmailMessage(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], [settings.HNI_SUPPORT_EMAIL_ID])
        email.content_subtype = "html"
        email.send()