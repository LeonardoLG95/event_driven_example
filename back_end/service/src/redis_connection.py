from redis_om import get_redis_connection, HashModel
from src.constants import REDIS_HOST

REDIS = get_redis_connection(host=REDIS_HOST, port=6379, decode_responses=True)


class Delivery(HashModel):
    budget: int = 0
    notes: str = ""

    class Meta:
        database = REDIS


class Event(HashModel):
    delivery_id: str = None
    type: str
    data: str

    class Meta:
        database = REDIS
