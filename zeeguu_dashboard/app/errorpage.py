from flask import app, render_template


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", e=e)


@app.errorhandler(401)
def invalid_credentials(e):
    return render_template("404.html", e=e)