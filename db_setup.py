import pymysql
import os

# SET your api keys as env vars
DB_USER =  os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')

connection = pymysql.connect(host='localhost',
                             user=DB_USER,
                             passwd=DB_PASSWORD)
try:
        with connection.cursor() as cursor:
                sql = "CREATE DATABASE IF NOT EXISTS crimemap"
                cursor.execute(sql)
                sql = """CREATE TABLE IF NOT EXISTS crimemap.crimes (
id int NOT NULL AUTO_INCREMENT,
latitude FLOAT(10,6),
longitude FLOAT(10,6),
date DATETIME,
category VARCHAR(50),
description VARCHAR(1000),
updated_at TIMESTAMP,PRIMARY KEY (id)
)"""
                cursor.execute(sql);
        connection.commit()
finally:
        connection.close()
