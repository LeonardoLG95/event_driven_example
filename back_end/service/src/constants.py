END_POINT = {
    "status": "/deliveries/{pk}/status",
    "create": "/deliveries/create",
    "event": "/event",
}

EVENT_ORDER = [
    "CREATE_DELIVERY",
    "INCREASE_BUDGET",
    "START_DELIVERY",
    "PICKUP_PRODUCTS",
    "DELIVER_PRODUCTS",
]

ERR_ID_NOT_FOUND = "Delivery ID not found."
ERR_DELIVERY_STARTED = "Delivery already started."
ERR_NOT_ENOUGH_BUDGET = "Not enough budget for this delivery."
ERR_NOT_ENOUGH_QUANTITY = "Not enough quantity for this delivery."

REDIS_HOST = (
    "redis"  # Docker host, this should be into an env, but this was a quick tutorial
)
