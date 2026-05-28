from backend.db.firebase_client import init_firebase, get_firestore

init_firebase()
db = get_firestore()
docs = db.collection("users").stream()
for d in docs:
    data = d.to_dict()
    desc = data.get("face_descriptor")
    if desc:
        uid = d.id
        name = data.get("name", "Unknown")
        print(f"User: {name} [{uid}] | Dims: {len(desc)}")
