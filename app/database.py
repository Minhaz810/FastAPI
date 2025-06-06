import psycopg2
from psycopg2.extras import RealDictCursor
import time

while True:
    try:
        conn = psycopg2.connect(host="localhost",database="fastapi_test",user="postgres",password="pgadmin",port=5432,cursor_factory=RealDictCursor)
        cusror = conn.cursor()
        print("Database Connection is successful!")
        break
    except Exception as e:
        print("Failed to connect database")
        print(e)
        time.sleep(2)