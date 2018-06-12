

# Zeeguu Dashboard


[![Coverage Status](https://coveralls.io/repos/github/RUGSoftEng/2018-ZeeguuDashboard/badge.svg?branch=fix%2Funit_testing)](https://coveralls.io/github/RUGSoftEng/2018-ZeeguuDashboard?branch=fix%2Funit_testing)

## What is Zeeguu and what is this project about? (Zeeguu Dashboard

Zeeguu is an innovative new tool for learning languages. Zeeguu allows its users to read articles in a foreign language while having real time translation at their finger tips. Zeeguu allows its users to undertake interactive exercises with words they needed translating.
Zeeguu supports learning five different languages (English, Dutch, German, Spanish and French) from three base languages (English, Dutch and Chinese).

The current Zeeguu system is not set up for teachers, individuals can sign up to the website and they can be added to classes manually by system admins. But an automated and graphically supported system is needed to facilitate teachers in running a class with Zeeguu. This brings us to the project at hand. The aim of the Zeeguu dashboard project is to extend the Zeeguu website's functionality in order to help teachers use Zeeguu in their classrooms. This functionally should include the creation, mangagement and analysis of classes and students.

## How to Install

 1. Clone this repo
 2. Make a python virtual environment with the following packages by running the command `pip3 install -r requirements.txt` and generate output suitable for a requirements file by running `pip freeze > requirements.txt`
 3. Set environment variables 'ZEEGUU_DASHBOARD_CONFIG' and 'API_PATH'. You can set 'ZEEGUU_DASHBOARD_CONFIG' to the path with default.cfg in the project. The API_PATH must include an ip and port. This is hidden to protect the API server. 
 4. Run using flask

For information of the project check out the documents directory!

- Zeeguu Dashboard Team

