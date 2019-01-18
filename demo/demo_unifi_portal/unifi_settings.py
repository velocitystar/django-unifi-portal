#################################################
#        UNIFI SETTINGS CONFIGURATION           #
#################################################

from django.core.urlresolvers import reverse_lazy

UNIFI_INSTALLED_APPS = [
    'material',
    'django_unifi_portal',
]

UNIFI_LOGIN_URL = '/unifi-portal/login'

UNIFI_TEMPLATE_CONTEXT_PROCESSORS = [
        'material.frontend.context_processors.modules',
        'django_unifi_portal.context_processor.unifi_context'
]

UNIFI_TEMPLATE_BUILTINS = 'material.templatetags.material_form'

UNIFI_AUTHENTICATION_BACKENDS = (
    # Django
    'django.contrib.auth.backends.ModelBackend',

)

# Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from facebook.
# Email is not sent by default, to get it, you must request the email permission:
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, about, email, birthday, gender, hometown, languages'
}

UNIFI_SERVER = "ac.arsvcs.co"
UNIFI_PORT = 8443
UNIFI_VERSION = 'v4'
UNIFI_SITE_ID = 'default'

# It's important to note that if this server is offsite, you need to have port 8443 forwarded through to it
UNIFI_SSID = 'Test'
UNIFI_LOGO = '<relative path under the static folder to the logo png>'

UNIFI_USER = "henry"
UNIFI_PASSWORD = "devel0pment"
UNIFI_TIMEOUT_MINUTES = 480

