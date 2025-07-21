from datetime import datetime
import json

from pyflink.datastream import StreamExecutionEnvironment
from pyflink.common import Types, Time, WatermarkStrategy
from pyflink.common.watermark_strategy import TimestampAssigner
from pyflink.datastream.connectors.kafka import KafkaSource, KafkaOffsetsInitializer
from pyflink.common.serialization import SimpleStringSchema
from pyflink.datastream.window import SessionWindowTimeGapExtractor

def create_kafka_source():
    return KafkaSource.builder() \
        .set_bootstrap_servers('localhost:9092') \
        .set_topics('green-trips') \
        .set_group_id('flink-session-group') \
        .set_starting_offsets(KafkaOffsetsInitializer.latest()) \
        .set_value_only_deserializer(SimpleStringSchema()) \
        .build()

class TripTimestampAssigner(TimestampAssigner):
    def extract_timestamp(self, value, record_timestamp):
        try:
            json_value = json.loads(value)
            dropoff_time = datetime.strptime(
                json_value['lpep_dropoff_datetime'], 
                '%Y-%m-%d %H:%M:%S'
            )
            return int(dropoff_time.timestamp() * 1000)
        except Exception as e:
            print(f"Error extracting timestamp: {e}")
            return record_timestamp

def parse_trip(json_str):
    try:
        data = json.loads(json_str)
        return {
            'PULocationID': int(data['PULocationID']),
            'DOLocationID': int(data['DOLocationID']),
            'lpep_pickup_datetime': data['lpep_pickup_datetime'],
            'lpep_dropoff_datetime': data['lpep_dropoff_datetime']
        }
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return None

def process_stream():
    env = StreamExecutionEnvironment.get_execution_environment()
    env.add_jars("D:\\flink\\flink-2.0.0-bin-scala_2.12\\flink-2.0.0\\lib\\flink-connector-kafka-4.0.0-2.0.jar")
 # Update this to your actual path

    kafka_source = create_kafka_source()

    watermark_strategy = WatermarkStrategy \
        .for_bounded_out_of_orderness(Time.seconds(5)) \
        .with_timestamp_assigner(TripTimestampAssigner())

    stream = env.from_source(
        source=kafka_source,
        watermark_strategy=watermark_strategy,
        source_name="Kafka Source"
    )

    processed_stream = (
        stream
        .map(lambda x: parse_trip(x), output_type=Types.MAP(Types.STRING(), Types.STRING()))
        .filter(lambda x: x is not None)
        .key_by(lambda x: (x['PULocationID'], x['DOLocationID']))
        .window(SessionWindowTimeGapExtractor.with_gap(Time.minutes(5)))
        .reduce(
            lambda a, b: {
                'PULocationID': a['PULocationID'],
                'DOLocationID': a['DOLocationID'],
                'count': a.get('count', 1) + b.get('count', 1),
                'start_time': min(a['lpep_dropoff_datetime'], b['lpep_dropoff_datetime']),
                'end_time': max(a['lpep_dropoff_datetime'], b['lpep_dropoff_datetime'])
            }
        )
    )

    processed_stream \
        .map(lambda x: f"Location Pair ({x['PULocationID']}, {x['DOLocationID']}): "
                      f"Count: {x['count']}, Duration: {x['start_time']} to {x['end_time']}"
             ) \
        .print()

    env.execute("Taxi Trip Sessionization")

if __name__ == '__main__':
    process_stream()
