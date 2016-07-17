import pymysql
import os

# SET your api keys as env vars
DB_USER =  os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

class DBHelper:
  def connect(self, database="crimemap"):
    return pymysql.connect(host='localhost',
              user=DB_USER,
              passwd=DB_PASSWORD,
              db=database)

  def get_all_inputs(self):
    connection = self.connect()
    try:
      query = "SELECT description FROM crimes;"
      with connection.cursor() as cursor:
        cursor.execute(query)
      return cursor.fetchall()
    finally:
      connection.close()
  def add_input(self, data):
    connection = self.connect()
    try:
      # The following introduces a deliberate security flaw. See section on SQL injection below
      query = "INSERT INTO crimes (description) VALUES (%s);"
      with connection.cursor() as cursor:
        cursor.execute(query,data)
        connection.commit()
    finally:
      connection.close()
  def clear_all(self):
    connection = self.connect()
    try:
      query = "DELETE FROM crimes;"
      with connection.cursor() as cursor:
        cursor.execute(query) 
        connection.commit()
    finally:
      connection.close()

  def add_crime(self, category, date, latitude, longitude, description):
    connection = self.connect()
    try:
      query = "INSERT INTO crimes (category, date, latitude, longitude, description) \
        VALUES (%s, %s, %s, %s, %s)"
      with connection.cursor() as cursor:
        cursor.execute(query, (category, date, latitude, longitude, description))   
        connection.commit() 
    except Exception as e:
      print(e) 
    finally:
      connection.close()
