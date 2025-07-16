from typing import List
from fastapi import APIRouter, HTTPException, status
from database.connection import db
from models.events import Event, EventUpdate
from bson.objectid import ObjectId
from typing import List

event_router = APIRouter(
    tags=["Events"]
)
events_collection = db["events"]


@event_router.get("/", response_model=List[Event])
def retrieve_all_events():
    events = list(events_collection.find({},{"_id":0}))
    return events


@event_router.get("/{id}", response_model=Event)
def retrieve_event(id: str):
        event = events_collection.find_one({"_id": ObjectId(id)})
        if event:
            event["id"] = str(event["_id"])
            del event["_id"]
            return event
        
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Event with supplied ID does not exist"
         )




@event_router.post("/new", response_model=dict)
def create_event(new_event: Event):
    event_dict = new_event.dict()
    result = events_collection.insert_one(event_dict)
    return {
        "message": "Event created successfully",
        "event_id": str(result.inserted_id)
    }


@event_router.delete("/{id}")
def delete_event(event_id: str):
    result = events_collection.delete_one({"_id":ObjectId(event_id)})

    if result.deleted_count ==0:
    
        raise HTTPException(
        status_code= status.HTTP_404_NOT_FOUND,
        detail = "Event with the supplied Id does not exist"
    )
    return{"message": "Event deleted"}

@event_router.delete("/")
def delete_all_events():
     result = events_collection.delete_many({})
     return {"message":f"Deleted {result.deleted_count} events"}
