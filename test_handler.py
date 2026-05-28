from backend.db.firebase_client import init_firebase
from backend.main import _handle_access_event
import backend.dependencies as dependencies
from backend.core.access_control import AccessController

def test():
    print("Testing Event Handler crash...")
    init_firebase()
    dependencies.access_controller = AccessController()
    
    try:
        _handle_access_event("cam_webcam", "UPMhWmMjMPcC0wts5E98", {
            "user_id": "UPMhWmMjMPcC0wts5E98",
            "name": "Fabrice",
            "role": "student",
            "status": "recognized",
            "is_live": True,
            "liveness_score": 0.99
        })
        print("Success! No crash.")
    except Exception as e:
        import traceback
        traceback.print_exc()

test()
