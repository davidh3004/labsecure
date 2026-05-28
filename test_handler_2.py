from backend.db.firebase_client import init_firebase
from backend.main import _handle_access_event
import backend.dependencies as dependencies
from backend.core.access_control import AccessController
from backend.utils.sim_clock import sim_clock

def test():
    print("Testing Event Handler crash at 08:30...")
    init_firebase()
    sim_clock.set("2026-03-23", 8, 30)
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
