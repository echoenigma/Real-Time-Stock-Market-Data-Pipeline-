# Real-Time Stock Market Data Pipeline

A real-time data pipeline to stream OHLC (Open, High, Low, Close) market data from MetaTrader 5 into Apache Kafka, then consume and store it in MySQL using Dockerized services. Enables SQL-based querying on live financial data.

---

## 🔧 Tech Stack

- **Programming:** Python, SQL 
- **Streaming & Storage:** Apache Kafka, MySQL  
- **Orchestration:** Docker, Docker Compose  
- **Broker/API:** MetaTrader 5

---

## ⚙️ Architecture

MetaTrader 5 (Producer on Host)  
→ Kafka Broker (Docker)  
→ Kafka Consumer (Docker)  
→ MySQL Database (Docker)

---

## 🚀 Features

- Streams real-time OHLC forex data using MetaTrader 5.
- Publishes messages to Apache Kafka via a Python producer.
- Kafka consumer ingests and stores data into a MySQL database inside Docker.
- Enables real-time analysis via SQL (e.g., volume spikes, price breaks).
- Fully containerized using Docker Compose for seamless deployment.

---

