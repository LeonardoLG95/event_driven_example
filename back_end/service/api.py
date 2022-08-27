from json import dumps, loads
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException


from src.event_actions import EVENT_ACTIONS, rebuild_state
from src.redis_connection import REDIS, Delivery, Event
from src.constants import END_POINT, ERR_ID_NOT_FOUND

APP = FastAPI()

# To allow React app connect to this app
APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@APP.get(END_POINT["status"])
async def get_state(pk: str) -> JSONResponse:
    state = loads(REDIS.get(f"delivery:{pk}"))

    if state is None:
        state = rebuild_state(pk)
    if state is None:
        raise HTTPException(status_code=404, detail=ERR_ID_NOT_FOUND)

    return JSONResponse(status_code=status.HTTP_200_OK, content=state)


@APP.post(END_POINT["create"])
async def create(request: Request) -> JSONResponse:
    body = await request.json()
    data = body["data"]

    delivery = Delivery(budget=data["budget"], notes=data["notes"]).save()

    event = Event(delivery_id=delivery.pk, type=body["type"], data=dumps(data)).save()

    state = EVENT_ACTIONS[event.type]({}, event)

    # Save in redis cache
    REDIS.set(f"delivery:{delivery.pk}", dumps(state))

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=state)


@APP.post(END_POINT["event"])
async def dispatch(request: Request) -> JSONResponse:
    body = await request.json()
    delivery_id = body["delivery_id"]

    event = Event(
        delivery_id=delivery_id, type=body["type"], data=dumps(body["data"])
    ).save()

    state = REDIS.get(f"delivery:{delivery_id}")
    if state is None:
        raise HTTPException(status_code=404, detail=ERR_ID_NOT_FOUND)

    new_state = EVENT_ACTIONS[event.type](loads(state), event)
    REDIS.set(f"delivery:{delivery_id}", dumps(new_state))

    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content=new_state)
