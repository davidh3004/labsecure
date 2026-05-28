import asyncio
from backend.db.firebase_client import init_firebase
from backend.db.repositories import UserRepository
from backend.utils.sim_clock import sim_clock

def test():
    print("Testing Firebase Init")
    init_firebase()
    print("Testing User Repository Descriptors")
    try:
        desc = UserRepository.get_all_descriptors()
        print(f"Loaded {len(desc)} descriptors")
    except Exception as e:
        print(f"Error loading desc: {e}")

test()
