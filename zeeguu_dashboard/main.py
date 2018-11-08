import os
import sys

from flask_bootstrap import Bootstrap

from zeeguu_teacher_dashboard import app

arguments = sys.argv
if len(arguments) > 0:
    for arg in arguments:
        if arg == 'Debug':
            app.debug = True

print(os.environ.get("ZEEGUU_DASHBOARD_CONFIG"))

app.config.from_pyfile(os.environ.get("ZEEGUU_DASHBOARD_CONFIG"), silent=False)
bootstrap = Bootstrap(app)

print("Running Teacher Dashboard with config: ")
print (app.config)

app.run(use_reloader=True)