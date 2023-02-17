import json
import psycopg2
import time
import os

conn = psycopg2.connect(os.environ["CONN_STRING"])
cursor = conn.cursor()

create_table_statement = """CREATE TABLE IF NOT EXISTS sensor_data (
        time TIMESTAMPTZ,
        location TEXT,
        temperature DOUBLE PRECISION
    );
    SELECT create_hypertable('sensor_data', 'time', if_not_exists => TRUE);
"""

cursor.execute(create_table_statement)
conn.commit()

def lambda_handler(event, context):
    cursor.execute("SELECT * FROM sensor_data ORDER BY time DESC LIMIT 5;")

    response = []

    rows = cursor.fetchall()
    for row in rows:
        response.append({
            "time": int(time.mktime(row[0].timetuple())),
            "location": row[1],
            "temperature": row[2]
        })

    return {
        "statusCode": 200,
        "body": json.dumps(response)
    }

