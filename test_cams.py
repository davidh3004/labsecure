from backend.db.firebase_client import init_firebase
from backend.db.repositories import CameraRepository

init_firebase()
cams = CameraRepository.get_all()
for c in cams:
    print(c)
