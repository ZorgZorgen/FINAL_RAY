from split_settings.tools import optional, include
import django_heroku
import dj_database_url
import os
import dotenv
import environ



from dotenv import load_dotenv, find_dotenv
import django_heroku
import dj_database_url

load_dotenv(find_dotenv())

#SECRET_KEY = env['SECRET_KEY']

# UPDATE secret key
SECRET_KEY = os.environ['SECRET_KEY'] # Instead of your actual secret key

MIDDLEWARE = [
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
]

include(
    'components/django_environ.py',
    'components/base.py',
    'components/django_phonenumber_field.py',
    'components/django_flex_user.py',
    'components/djangorestframework.py',
    'components/drf_multiple_model.py',
    'components/social_auth_app_django.py',
    'components/sendgrid.py',
    optional('local_settings.py')
)

# Had to add test_runner = False to fix GitHub actions bug
# https://travis-ci.community/t/django-unit-tests-failing-on-travis-builds/10625
django_heroku.settings(locals(), test_runner=False)

MONGODB_DATABASES = {
    "default": {
        "name": 'UsuariosDB',
        "host": 'localhost',
        "password": 'B@$3dwhat123',
        "username": 'root',
        "tz_aware": True, # if you using timezones in django (USE_TZ = True)
    },
}


SESSION_ENGINE = 'redis_sessions.session'

SESSION_REDIS = {
    'host': 'localhost',
    'port': 6379,
    'db': 0,
    'password': 'password',
    'prefix': 'session',
    'socket_timeout': 1,
    'retry_on_timeout': False
    }
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_flex_user.apps.DjangoFlexUserConfig',
    'rest_framework', 
    'rest_framework.authtoken', 
    'drf_multiple_model', 
    'social_django',
    
]

#SOCIAL_AUTH_STORAGE = 'social_django_mongoengine.models.DjangoStorage'

SOCIAL_AUTH_JSONFIELD_ENABLED = True

AUTHENTICATION_BACKENDS = (
    'django_flex_user.backends.FlexUserModelBackend',
    'django_flex_user.backends.FlexUserFacebookOAuth2', # Add me
    'django_flex_user.backends.FlexUserGoogleOAuth2',


    # Facebook OAuth2
    'social_core.backends.facebook.FacebookAppOAuth2',
    'social_core.backends.facebook.FacebookOAuth2',

    # django-rest-framework-social-oauth2
    'rest_framework_social_oauth2.backends.DjangoOAuth2',

    # Django
    'django.contrib.auth.backends.ModelBackend',
)

# Facebook configuration
SOCIAL_AUTH_FACEBOOK_KEY = '587470876089390'
SOCIAL_AUTH_FACEBOOK_SECRET = 'f23663b5d1e4bb5b7701281cda415807'

# Define SOCIAL_AUTH_FACEBOOK_SCOPE to get extra permissions from Facebook.
# Email is not sent by default, to get it, you must request the email permission.
SOCIAL_AUTH_FACEBOOK_SCOPE = ['email']
SOCIAL_AUTH_FACEBOOK_PROFILE_EXTRA_PARAMS = {
    'fields': 'id, name, email'
}



AUTH_USER_MODEL = 'django_flex_user.FlexUser'

SOCIAL_AUTH_CLEAN_USERNAME_FUNCTION = 'django_flex_user.validators.flex_user_clean_username'

# Pipeline configuration

SOCIAL_AUTH_PIPELINE = (

    # Get the information we can about the user and return it in a simple

    # format to create the user instance later. On some cases the details are

    # already part of the auth response from the provider, but sometimes this

    # could hit a provider API.

    'social_core.pipeline.social_auth.social_details',


    # Get the social uid from whichever service we're authing thru. The uid is

    # the unique identifier of the given user in the provider.

    'social_core.pipeline.social_auth.social_uid',


    # Verifies that the current auth process is valid within the current

    # project, this is where emails and domains whitelists are applied (if

    # defined).

    'social_core.pipeline.social_auth.auth_allowed',


    # Checks if the current social-account is already associated in the site.

    'social_core.pipeline.social_auth.social_user',


    # Make up a username for this person, appends a random string at the end if

    # there's any collision.

    'social_core.pipeline.user.get_username',


    # Send a validation email to the user to verify its email address.

    'django_flex_user.verification.mail_validation',


    # Associates the current social details with another user account with

    # a similar email address.

    'social_core.pipeline.social_auth.associate_by_email',


    # Create a user account if we haven't found one yet.

    'social_core.pipeline.user.create_user',


    # Create the record that associated the social account with this user.

    'social_core.pipeline.social_auth.associate_user',


    # Populate the extra_data field in the social record with the values

    # specified by settings (and the default ones like access_token, etc).

    'social_core.pipeline.social_auth.load_extra_data',


    # Update the user record with any changed info from the auth service.

    'social_core.pipeline.user.user_details'

)


SOCIAL_AUTH_EMAIL_VALIDATION_FUNCTION = 'apps.main.mail.send_validation'
SOCIAL_AUTH_EMAIL_VALIDATION_URL = '/email_sent/'
SOCIAL_AUTH_FORCE_EMAIL_VALIDATION = True

DEBUG = True

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
django_heroku.settings(locals())

ALLOWED_HOSTS = ['localhost']