from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StringType, FloatType, LongType

# Define schema for the soccer events
schema = StructType() \
    .add("player_id", StringType()) \
    .add("team", StringType()) \
    .add("event_type", StringType()) \
    .add("location", StructType().add("x", FloatType()).add("y", FloatType())) \
    .add("time", LongType())

def process_data(df, batch_id):
    """Processing function to handle incoming streaming data."""
    df.show()  # Placeholder for actual transformations
    # Save or process data further (e.g., storing into BigQuery/Redshift)

if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("SoccerAnalytics") \
        .getOrCreate()

    # Read from Kafka
    raw_data = spark.readStream \
        .format("kafka") \
        .option("kafka.bootstrap.servers", "localhost:9092") \
        .option("subscribe", "soccer-match-events") \
        .load()

    # Convert value column from Kafka (binary) to string, then JSON
    json_data = raw_data.selectExpr("CAST(value AS STRING)") \
                        .select(from_json(col("value"), schema).alias("data")) \
                        .select("data.*")

    # Apply transformations and output to console or storage
    query = json_data.writeStream \
        .outputMode("append") \
        .foreachBatch(process_data) \
        .start()

    query.awaitTermination()
