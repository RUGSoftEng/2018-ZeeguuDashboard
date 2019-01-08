#!/usr/bin/env python
# -*- coding: utf8 -*-

import setuptools

setuptools.setup(
    name="zeeguu_teacher_dashboard",
    version="0.1",
    packages=setuptools.find_packages(),
    include_package_data=True,
    zip_safe=False,
    author="",
    author_email="",
    description="Teacher Dashboard for Zeeguu",
    keywords="",
    dependency_links=[],
    install_requires=(
        "Flask",
        "Flask-WTF",
        "Flask-Migrate",
        "Flask-SQLAlchemy",
        "Jinja2",
        "WTForms",
        "requests",
        "Werkzeug",
        "mysqlclient",
        "pytest",
        "pytest-cov",
        "coveralls"
    ),
)
