# NYC Green Taxi Real-Time Streaming Pipeline 📊

A **real-time data streaming pipeline** using **Apache Flink**, **Redpanda (Kafka-compatible)**, and **PostgreSQL** to simulate and analyze high-velocity transportation data from the **NYC Green Taxi trip dataset**.

This project demonstrates a production-grade architecture for **stream processing**, **event-driven data engineering**, and **urban mobility analytics** using open-source tools and containerized deployment.

---

## 🚀 Project Highlights

- Real-time ingestion and processing of NYC taxi trip data
- Event-time **session windowing** to detect uninterrupted travel patterns
- Kafka-compatible producer using Python (`kafka-python`)
- Stream processing using Apache Flink
- Processed data persistence in PostgreSQL for downstream querying
- Local deployment using Docker Compose

---

## 🛠️ Tech Stack

| Tool          | Purpose                                                  |
|---------------|----------------------------------------------------------|
| **Redpanda**  | Kafka-compatible message broker                          |
| **Apache Flink** | Real-time stream processing with session windowing    |
| **PostgreSQL**| Data sink for storing processed events                   |
| **Docker Compose** | Orchestration of local development environment     |
| **Pandas**    | Dataset preprocessing                                    |
| **kafka-python** | Kafka producer implementation in Python              |
| **DBeaver** *(optional)* | PostgreSQL GUI client                         |

---

## 📁 Project Structure

```bash
nyc-green-taxi-streaming/
├── docker-compose.yml       # Service definitions for Redpanda, Flink, PostgreSQL
├── load_taxi_data.py        # Kafka producer for simulating trip data
├── session_job.py           # Apache Flink job for session windowing
├── README.md                # Project documentation
└── data/                    # Directory to place NYC Green Taxi CSV file
````

---

## 🔧 Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/nyc-green-taxi-streaming.git
cd nyc-green-taxi-streaming
```

### 2. Add Dataset

Download the **October 2019 NYC Green Taxi CSV file** from the [NYC TLC website](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page) and place it in the `data/` folder.

---

## 🚀 Running the Project

### 1. Launch the Services

```bash
docker-compose up -d
```

This starts:

* Redpanda (Kafka-compatible broker) → `localhost:9092`
* Apache Flink Dashboard → [http://localhost:8081](http://localhost:8081)
* PostgreSQL → `localhost:5432` (username: `postgres`, password: `postgres`)

---

### 2. Stream Data into Kafka

Run the Python producer to publish taxi trip records to the Kafka topic:

```bash
python load_taxi_data.py
```

This streams trip data to the topic `green-trips`.

---

### 3. Submit the Flink Job

Go to the Flink Dashboard [http://localhost:8081](http://localhost:8081) and submit `session_job.py`.

Session window configuration:

* **Session gap:** 5 minutes
* **Watermark delay:** 5 seconds
* **Event time field:** `lpep_dropoff_datetime`

---

### 4. Query Processed Results

Apache Flink outputs results to PostgreSQL.

Sample schema:

```sql
CREATE TABLE processed_events (
  test_data INTEGER,
  event_timestamp TIMESTAMP
);
```

You can query the table using:

* `psql`
* `DBeaver`
* BI tools (e.g., Superset, Looker Studio)

---

## 📈 Use Cases

* Real-time ETL and stream processing
* Urban traffic and fleet optimization
* Event-driven architecture modeling
* Hands-on learning for Apache Flink & Kafka
* Portfolio-ready project for aspiring data engineers

---

## ✅ Prerequisites

* Python 3.7+
* Docker & Docker Compose
* NYC Green Taxi CSV file (October 2019)

---

## 📎 Resources

* [Redpanda Docs](https://docs.redpanda.com/)
* [Apache Flink Docs](https://nightlies.apache.org/flink/)
* [NYC Taxi Dataset](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
* [PostgreSQL Docs](https://www.postgresql.org/docs/)

---

## 🤝 Contributing

Pull requests and contributions are welcome. Please open an issue to discuss your idea first.

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 📬 Contact

**Author:** Faizan Mahmood
**Email:** [faizanworkmail1@gmail.com](mailto:your.email@example.com)
**LinkedIn:** [https://www.linkedin.com/in/m-faizan-mahmood](https://www.linkedin.com/in/m-faizan-mahmood)

---

⭐️ **If you found this project useful, don't forget to star it!**
