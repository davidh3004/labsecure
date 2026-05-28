import asyncio
from backend.db.firebase_client import init_firebase
from backend.db.repositories import EventRepository, _now
from backend.db.schemas import EventCreate, EventType, EventSeverity

def test():
    print("Testing Firebase init")
    init_firebase()
    print("Testing _now()")
    try:
        n = _now()
        print(f"Now: {n} (type {type(n)})")
    except Exception as e:
        print("Error _now:", e)
        return
        
    print("Testing EventRepository.create")
    try:
        ev = EventRepository.create(EventCreate(
            type=EventType.ACCESS_GRANTED,
            user_id="test",
            camera_id="cam_test",
            details={},
            severity=EventSeverity.INFO
        ))
        print("Event Created", ev)
    except Exception as e:
        print("Error Event:", e)

test()
