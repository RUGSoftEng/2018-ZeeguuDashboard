import os
import sys
from flask_bootstrap import Bootstrap

from app import app

arguments = sys.argv
if len(arguments) > 0:
    for arg in arguments:
        if arg == 'Debug':
            app.debug = True


app.config.from_pyfile(os.environ.get("ZEEGUU_DASHBOARD_CONFIG"), silent=False)
app.config["API_PATH"] = os.environ.get("API_PATH")
bootstrap = Bootstrap(app)

app.run()
