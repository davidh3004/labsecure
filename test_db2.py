from backend.db.firebase_client import init_firebase
from backend.db.repositories import UserRepository
import numpy as np

def test():
    init_firebase()
    desc = UserRepository.get_all_descriptors()
    print("Descriptors loaded:", len(desc))
    for entry in desc:
        uid = entry["user_id"]
        d = entry.get("descriptor")
        print(f"User {entry['name']} ({entry.get('role')}): desc type {type(d)}, length {len(d) if d else 'None'}")
        
    face_db = {}
    for entry in desc:
        uid = entry["user_id"]
        d = entry.get("descriptor")
        if d and len(d) == 512:
            face_db[uid] = np.array(d, dtype=np.float32)
    print("face_db keys:", list(face_db.keys()))

test()
