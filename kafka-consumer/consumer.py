from kafka import KafkaConsumer
import json
import mysql.connector
import time

time.sleep(10)  # Wait for MySQL to be ready

# Connect to MySQL inside Docker
conn = mysql.connector.connect(
    host='mysql',      # service name from docker-compose
    port=3306,
    user='root',
    password='root',
    database='trading_data'
)

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS ohlc (
    id INT AUTO_INCREMENT PRIMARY KEY,
    time DATETIME,
    open DOUBLE,
    high DOUBLE,
    low DOUBLE,
    close DOUBLE,
    volume INT
)
""")

consumer = KafkaConsumer(
    'ohlc-data',
    bootstrap_servers='kafka:29092', # <- use this for containers inside Docker,  # also Docker service name
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest',
    enable_auto_commit=True
)

print("Kafka Consumer started inside Docker.")

for message in consumer:
    data = message.value
    print("Received:", data)

    cursor.execute("""
        INSERT INTO ohlc (time, open, high, low, close, volume)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (
        data['time'], data['open'], data['high'],
        data['low'], data['close'], data['volume']
    ))
    conn.commit()
