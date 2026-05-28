from backend.db.firebase_client import init_firebase
from backend.db.repositories import UserRepository

init_firebase()

users = UserRepository.get_all(active_only=False)
for u in users:
    if u.descriptors:
        print(f"[{u.name}] ID: {u.id} | Dims: {u.descriptors[0].get('dimension', 'unknown') if u.descriptors else 0}")
    else:
        print(f"[{u.name}] ID: {u.id} | NO DESCRIPTOR")
