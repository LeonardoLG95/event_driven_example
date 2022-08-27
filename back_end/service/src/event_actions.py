"""Data consumed by the front-end"""
from fastapi.exceptions import HTTPException
from json import loads
from src.redis_connection import Event
from src.constants import (
    EVENT_ORDER,
    ERR_DELIVERY_STARTED,
    ERR_NOT_ENOUGH_BUDGET,
    ERR_NOT_ENOUGH_QUANTITY,
)


def create_delivery(_: dict, event: Event) -> dict:
    data = loads(event.data)
    return {
        "id": event.delivery_id,
        "budget": data["budget"],
        "notes": data["notes"],
        "status": "ready",
    }


def start_delivery(state: dict, _: Event) -> dict:
    if state["status"] != "ready":
        raise HTTPException(status_code=400, detail=ERR_DELIVERY_STARTED)

    start_state = state | {"status": "active"}
    return start_state


def pickup_products(state: dict, event: Event) -> dict:
    data = loads(event.data)
    purchase_price = float(data["purchase_price"])
    quantity = float(data["quantity"])
    new_budget = float(state["budget"]) - purchase_price * quantity

    if new_budget < 0:
        raise HTTPException(status_code=400, detail=ERR_NOT_ENOUGH_BUDGET)

    return state | {
        "budget": new_budget,
        "purchase_price": purchase_price,
        "quantity": quantity,
        "status": "collected",
    }


def deliver_products(state: dict, event: Event) -> dict:
    data = loads(event.data)
    sell_price = float(data["sell_price"])
    quantity = float(data["quantity"])
    new_budget = float(state["budget"]) + sell_price * quantity
    new_quantity = float(state["quantity"]) - quantity

    if new_quantity < 0:
        raise HTTPException(status_code=400, detail=ERR_NOT_ENOUGH_QUANTITY)

    return state | {
        "budget": new_budget,
        "sell_price": sell_price,
        "quantity": new_quantity,
        "status": "completed",
    }


def increase_budget(state: dict, event: Event) -> dict:
    data = loads(event.data)
    state["budget"] = float(state["budget"]) + float(data["budget"])

    return state


EVENT_ACTIONS = {
    "CREATE_DELIVERY": create_delivery,
    "START_DELIVERY": start_delivery,
    "PICKUP_PRODUCTS": pickup_products,
    "DELIVER_PRODUCTS": deliver_products,
    "INCREASE_BUDGET": increase_budget,
}


def rebuild_state(pk: str) -> dict:
    if pk is None:
        return

    pks = Event.all_pks()

    all_events = [Event.get(pk) for pk in pks]
    events = [event for event in all_events if event.delivery_id == pk]
    if not events:
        return

    ordered_events = []
    for event_type in EVENT_ORDER:
        for event in events:
            if event.type == event_type:
                ordered_events.append(event)
                # More conditions can be added to have the proper event in case of duplicates
                break

    state = {}
    for event in ordered_events:
        state = EVENT_ACTIONS[event.type](state, event)

    return state
