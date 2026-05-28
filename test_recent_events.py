from backend.db.firebase_client import init_firebase
from backend.db.repositories import EventRepository

def test():
    init_firebase()
    print("Fetching recent events...")
    docs = EventRepository.query(limit=10)
    for d in docs:
        print(f"[{d.timestamp}] {d.type} | User: {d.user_id} | Details: {d.details}")

test()
