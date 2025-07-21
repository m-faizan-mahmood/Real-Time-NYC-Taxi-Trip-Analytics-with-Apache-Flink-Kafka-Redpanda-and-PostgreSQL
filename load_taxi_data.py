import pandas as pd
import json
import time
from kafka import KafkaProducer

# Step 1: Load the data
df = pd.read_csv('green_tripdata_2019-10.csv.gz', compression='gzip')

# Step 2: Select required columns
cols = [
    'lpep_pickup_datetime',
    'lpep_dropoff_datetime',
    'PULocationID',
    'DOLocationID',
    'passenger_count',
    'trip_distance',
    'tip_amount'
]
df_green = df[cols]

# Step 3: Create Kafka Producer
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda data: json.dumps(data).encode('utf-8')
)

# Step 4: Send rows to Kafka
start_time = time.time()

for row in df_green.itertuples(index=False):
    row_dict = {col: getattr(row, col) for col in row._fields}
    producer.send('green-trips', value=row_dict)

# Make sure everything is sent
producer.flush()

end_time = time.time()

# Calculate duration
total_time = round(end_time - start_time)
print(f"✅ Sent {len(df_green)} messages in {total_time} seconds")