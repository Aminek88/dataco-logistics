from pydantic import BaseModel

class LogisticData(BaseModel):
    order_id: str
    departure_date: str
    arrival_date: str
    quantity: int
    warehouse_location: str
    delivery_location: str