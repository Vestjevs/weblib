CSRF_ENABLED = True

try:
    DATABASE_URL = os.environ['DATABASE_URL']
except:
    DATABASE_URL = 'sqlite:///sqlite.db'

# RECAPTCHA_PUBLIC_KEY = '#############'
