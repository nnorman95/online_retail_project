import psycopg

conn = psycopg.connect("dbname=online_retail_project user=norman")
cur = conn.cursor()

cur.execute("SELECT current_database(), current_user")
result = cur.fetchone()

print(result)

conn.close()