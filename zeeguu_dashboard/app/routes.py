from flask import render_template, flash, redirect
from app import app


@app.route('/')
def template():
	return render_template('navbar.html', title='Zeeguu2.0')