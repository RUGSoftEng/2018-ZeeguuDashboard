import os
import sys

from zeeguu_teacher_dashboard import app as application

# when running as WSGI environment variables can't be set
# for such a case we expect the env_var_defs.py in the 
# same folder as the wsgi script to export the required 
# envvars 

try:
    import env_var_defs
    print ("found the env_var_defs file")
except:
    print ("didn't find env_var_defs. hopefully there's envvars defined")


application.config.from_pyfile(os.environ['TEACHER_DASHBOARD_CONFIG'], silent=False)

from raven.contrib.flask import Sentry
sentry = Sentry(application, dsn=application.config['SENTRY_DSN'])


print("Runnning the teacher dashboard with config: ")
print (application.config)

