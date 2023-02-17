import json
import psycopg2
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
    body = json.loads(event["body"])

    temperature = body["temperature"]
    location = body["location"]

    print(temperature, location)

    cursor.execute("""INSERT INTO sensor_data 
        (time, location, temperature) VALUES (NOW(), %s, %s);
        """, (location, temperature))

    conn.commit()

    return {
        "statusCode": 200
    }
