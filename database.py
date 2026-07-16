import pymysql
from pymongo import MongoClient
from config import *

def get_mysql_connection():
    return pymysql.connect(
        host=MYSQL_HOST,
        port=MYSQL_PORT,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client["conversation_ai"]
memory_collection = mongo_db["memory"]