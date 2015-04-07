#coding:UTF-8

from sqlalchemy import create_engine

MYSQL_HOST="127.0.0.1"
MYSQL_PORT="3306"
MYSQL_USER="root"
MYSQL_PASSWORD="root"
MYSQL_DB="calender"

db=create_engine("mysql://%s:%s@%s/%s?charset=utf8&use_unicode=0"%(MYSQL_USER,MYSQL_PASSWORD,MYSQL_HOST,MYSQL_DB),echo=True)


