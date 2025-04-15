from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import snowflake.connector
import os
from dotenv import load_dotenv
import pandas as pd
from confluent_kafka import Producer
import json

app = FastAPI()
load_dotenv()

# Snowflake connection
def get_snowflake_conn():
    return snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA")
    )

# Kafka producer
kafka_conf = {"bootstrap.servers": "kafka:9092"}
producer = Producer(kafka_conf)

class LogisticData(BaseModel):
    order_id: str
    departure_date: str
    arrival_date: str
    quantity: int
    warehouse_location: str
    delivery_location: str

@app.post("/api/logistics/load")
async def load_logistics():
    try:
        # Lire le CSV (à ajuster si le nom est différent)
        df = pd.read_csv("/app/data/logistics_data.csv")
        # Valider les colonnes
        required_columns = ["Order Id", "order date (DateOrders)", "shipping date (DateOrders)", "Order Item Quantity", "Customer City", "Order City"]
        if not all(col in df.columns for col in required_columns):
            raise HTTPException(status_code=400, detail="CSV missing required columns")
        # Mapper les données
        df_mapped = pd.DataFrame({
            "order_id": df["Order Id"],
            "departure_date": df["order date (DateOrders)"],
            "arrival_date": df["shipping date (DateOrders)"],
            "quantity": df["Order Item Quantity"],
            "warehouse_location": df["Customer City"],
            "delivery_location": df["Order City"]
        })
        # Se connecter à Snowflake
        conn = get_snowflake_conn()
        try:
            cursor = conn.cursor()
            cursor.execute("TRUNCATE TABLE logistics")
            # Charger les données
            for _, row in df_mapped.iterrows():
                cursor.execute(
                    "INSERT INTO logistics (order_id, departure_date, arrival_date, quantity, warehouse_location, delivery_location) VALUES (%s, %s, %s, %s, %s, %s)",
                    (
                        row["order_id"],
                        row["departure_date"],
                        row["arrival_date"],
                        int(row["quantity"]),
                        row["warehouse_location"],
                        row["delivery_location"]
                    )
                )
                # Publier dans Kafka
                producer.produce("logistics-topic", json.dumps(row.to_dict()).encode("utf-8"))
            conn.commit()
            producer.flush()
            return {"message": f"Loaded {len(df_mapped)} records into Snowflake and Kafka"}
        finally:
            conn.close()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/logistics")
async def get_logistics():
    conn = get_snowflake_conn()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT order_id, departure_date, arrival_date, quantity, warehouse_location, delivery_location FROM logistics")
        results = cursor.fetchall()
        return [
            {
                "order_id": row[0],
                "departure_date": str(row[1]),
                "arrival_date": str(row[2]),
                "quantity": row[3],
                "warehouse_location": row[4],
                "delivery_location": row[5]
            }
            for row in results
        ]
    finally:
        conn.close()

@app.post("/api/logistics")
async def post_logistics(data: LogisticData):
    producer.produce("logistics-topic", json.dumps(data.dict()).encode("utf-8"))
    producer.flush()
    conn = get_snowflake_conn()
    try:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO logistics (order_id, departure_date, arrival_date, quantity, warehouse_location, delivery_location) VALUES (%s, %s, %s, %s, %s, %s)",
            (
                data.order_id,
                data.departure_date,
                data.arrival_date,
                data.quantity,
                data.warehouse_location,
                data.delivery_location
            )
        )
        conn.commit()
        return {"message": "Data processed", "data": data}
    finally:
        conn.close()