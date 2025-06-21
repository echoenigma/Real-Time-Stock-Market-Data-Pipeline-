import MetaTrader5 as mt5
from kafka import KafkaProducer
import pandas as pd
import time
import json
from datetime import datetime

# --- MetaTrader 5 credentials ---
login_id = 5036952413
password = "U_Co5zJc"
server = "MetaQuotes-Demo"

# --- Initialize MT5 ---
print("Connecting to MetaTrader 5...")
if not mt5.initialize(login=login_id, password=password, server=server):
    print("Initialization failed!", mt5.last_error())
    mt5.shutdown()
    exit()
else:
    print("Connected to MT5")

# --- Select symbol ---
symbol = "EURUSD"
if not mt5.symbol_select(symbol, True):
    print(f"Failed to select symbol: {symbol}")
    mt5.shutdown()
    exit()

# --- Initialize Kafka Producer ---
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)
print("Kafka Producer initialized.")

# --- Infinite loop to send data ---
try:
    while True:
        print("\nFetching data at", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        ohlc = mt5.copy_rates_from_pos(symbol, mt5.TIMEFRAME_M1, 0, 1)
        if ohlc is None or len(ohlc) == 0:
            print("Failed to fetch OHLC data")
        else:
            df = pd.DataFrame(ohlc)
            df['time'] = pd.to_datetime(df['time'], unit='s')
            row = df.iloc[0]

            ohlc_data = {
    "time": str(row['time']),
    "open": float(row['open']),
    "high": float(row['high']),
    "low": float(row['low']),
    "close": float(row['close']),
    "volume": int(row['tick_volume'])
}


            print("Sending to Kafka:", ohlc_data)
            producer.send('ohlc-data', value=ohlc_data)

        time.sleep(60)

except KeyboardInterrupt:
    print("Script manually stopped.")

finally:
    mt5.shutdown()
    print("Disconnected from MT5")
