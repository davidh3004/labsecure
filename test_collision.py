import cv2
import numpy as np
from backend.db.firebase_client import init_firebase
from backend.db.repositories import UserRepository
from backend.vision.face_engine import FaceEngine

def test():
    init_firebase()
    
    # Load Database
    descriptors = UserRepository.get_all_descriptors()
    face_db = {}
    user_info = {}
    
    for entry in descriptors:
        uid = entry["user_id"]
        desc = entry.get("descriptor")
        if not desc or len(desc) != 512:
            continue
        face_db[uid] = np.array(desc, dtype=np.float32)
        user_info[uid] = {"name": entry.get("name", "Unknown")}
        
    print(f"Loaded {len(face_db)} valid 512-dim descriptors.")
    
    # Init Engine
    print("Initialising FaceEngine...")
    engine = FaceEngine(model_name="buffalo_sc")
    
    # Capture Frame
    print("Capturing from Webcam...")
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print("Failed to grab camera frame.")
        return
        
    faces = engine.detect(frame)
    if not faces:
        print("No faces detected in the current physical frame.")
        return
        
    for i, f in enumerate(faces):
        emb = f.get("embedding")
        if emb is None:
            continue
            
        norm_emb = emb / np.linalg.norm(emb)
        print(f"\nDetected Face {i}:")
        scores = []
        for uid, db_emb in face_db.items():
            norm_db = db_emb / np.linalg.norm(db_emb)
            sim = np.dot(norm_emb, norm_db)
            scores.append((sim, user_info.get(uid, {}).get("name")))
            
        scores.sort(key=lambda x: x[0], reverse=True)
        for s, name in scores:
            print(f" -> Score: {s:.4f}  |  User: {name}")

test()
