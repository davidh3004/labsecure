from backend.db.firebase_client import init_firebase
from backend.api.cameras import _rebuild_id_map, _id_map

init_firebase()
_rebuild_id_map()
print("ID MAP:")
print(_id_map)
