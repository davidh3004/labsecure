from backend.db.firebase_client import init_firebase
from backend.api.schedules import get_attendance
import traceback

init_firebase()

try:
    print("Fetching attendance...")
    res = get_attendance("bKEmHmiF2anm2FBL18hc", "2026-03-23")
    print(res)
except Exception as e:
    traceback.print_exc()
