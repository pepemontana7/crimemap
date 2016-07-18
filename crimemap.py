from flask import Flask
from flask import render_template
from flask import request
import json
import os
import datetime
import dateparser
import string

categories = ['mugging', 'break-in']
TEST = os.environ.get('TEST_CRIMEAPP')
if TEST == True:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    from dbhelper import DBHelper

app = Flask(__name__)
DB = DBHelper()

@app.route("/")
def home(error_message=None):
    crimes = json.dumps(DB.get_all_crimes())
    return render_template("home.html", crimes=crimes, categories=categories, error_message=error_message)

@app.route("/submitcrime", methods=['POST'])
def submitcrime():
  category = request.form.get("category")
  if category not in categories:
      return home()
  date = format_date(request.form.get("date") )
  if not date:
      return home("Invalid date. Please use yyyy-mm-dd format")
  try:
      latitude = float(request.form.get("latitude"))
      longitude = float(request.form.get("longitude"))
  except ValueError:
      return home()
  description = request.form.get("description") 
  description = sanitize_string(request.form.get("description"))
  DB.add_crime(category, date, latitude, longitude, description)
  return home()

def format_date(userdate):
    date = dateparser.parse(userdate)
    try:
        return datetime.datetime.strftime(date, "%Y-%m-%d")
    except TypeError:
        return None  

def sanitize_string(userinput):
    whitelist = string.letters + string.digits + " !?$.,;:-'()&"
    return filter(lambda x: x in whitelist, userinput)  

if __name__ == '__main__':
  app.run(host='0.0.0.0', port=5000, debug=True)
