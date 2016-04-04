import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = "2d1484bc-aaa2-4bd4-b0b3-f4e0ddcffb35a9491e47-b954-4db5-95b9-785e3fbfb4dfa4c472eb-f860-435d-befc-a89fef91bd2a"
NEVERCACHE_KEY = "b684ed01-74f6-4d90-8162-9d21df32b7d626a180f0-b9fd-4de1-98e5-18166c6f9dec27faf333-53cd-4931-a14e-06ca6080f8de"
ALLOWED_HOSTS = ["www.a2b.am", "a2b.am"]

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

#production
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.postgresql_psycopg2',
    'NAME': 'a2b',
    'USER': 'a2b',
    'PASSWORD': 'aaa',
    'HOST': 'localhost',
    'PORT': '',
}
}

#staging
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'staging_a2b',
#         'USER': '_staging_a2b',
#         'PASSWORD': 'aaa',
#         'HOST': 'localhost',
#         'PORT': '',
#     }
# }

#production
# FABRIC = {
#      "SSH_USER": "flaunt", # SSH username
#      "SSH_PASS":  "", # SSH password (consider key-based authentication)
#      "SSH_KEY_PATH":  "/home/bamby/.ssh/id_rsa.pub", # Local path to SSH key file, for key-based auth
#      "HOSTS": ["188.166.7.218"],
#      "DOMAINS": ALLOWED_HOSTS, # List of hosts to deploy to
#      "VIRTUALENV_HOME":  "/home/flaunt/virtenv", # Absolute remote path for virtualenvs
#      "PROJECT_NAME": "a2b", # Unique identifier for project
#      "REQUIREMENTS_PATH": "requirements.txt", # Path to pip requirements, relative to project
#      "GUNICORN_PORT": 8000, # Port gunicorn will listen on
#      "LOCALE": "en_US.UTF-8", # Should end with ".UTF-8"
#      "LIVE_HOSTNAME": "a2b", # Host for public site.
#      "REPO_URL": "https://github.com/davit-gh/a2b.git", # Git or Mercurial remote repo URL for the project
#      "DB_PASS": "thisisaproductiondatabase", # Live database password
#      "ADMIN_PASS": "scanyoga", # Live admin user password
#      "SECRET_KEY": SECRET_KEY,
#      "NEVERCACHE_KEY": NEVERCACHE_KEY,
# }

#staging
FABRIC = {
     "SSH_USER": "flaunt", # SSH username
     "SSH_PASS":  "", # SSH password (consider key-based authentication)
     "SSH_KEY_PATH":  "/home/bamby/.ssh/id_rsa.pub", # Local path to SSH key file, for key-based auth
     "HOSTS": ["188.166.7.218"],
     "DOMAINS": ['katnaratschool.xyz'], # List of hosts to deploy to
     "VIRTUALENV_HOME":  "/home/flaunt/staging_virtenv", # Absolute remote path for virtualenvs
     "PROJECT_NAME": "staging_a2b", # Unique identifier for project
     "REQUIREMENTS_PATH": "requirements.txt", # Path to pip requirements, relative to project
     "GUNICORN_PORT": 8000, # Port gunicorn will listen on
     "LOCALE": "en_US.UTF-8", # Should end with ".UTF-8"
     "LIVE_HOSTNAME": "staging_a2b", # Host for public site.
     "REPO_URL": "https://github.com/davit-gh/a2b.git", # Git or Mercurial remote repo URL for the project
     "DB_PASS": "thisisaproductiondatabase", # Live database password
     "ADMIN_PASS": "scanyoga", # Live admin user password
     "SECRET_KEY": SECRET_KEY,
     "NEVERCACHE_KEY": NEVERCACHE_KEY,
}
TEMPLATE_DEBUG = True

FORMS_USE_HTML5 = True
ACCOUNTS_MIN_PASSWORD_LENGTH = 6
ACCOUNTS_VERIFICATION_REQUIRED = False
ACCOUNTS_APPROVAL_REQUIRED = False