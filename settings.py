# settings for migrations check

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.sites",
    "pinax.referrals",
    "pinax.referrals.tests"
]
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": "db.sqlite3",
    }
}
SITE_ID = 1
ROOT_URLCONF = "pinax.referrals.tests.urls"
SECRET_KEY = "notasecret"
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
    },
]
