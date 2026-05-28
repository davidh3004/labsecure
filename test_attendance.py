import urllib.request
import json
import urllib.parse
from datetime import datetime, timezone

def get_json(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def test():
    try:
        # Date is 2026-03-23
        url = "http://127.0.0.1:8000/api/schedules/bKEmHmiF2anm2FBL18hc/attendance?date=2026-03-23"
        print(f"Fetching {url}...")
        res = get_json(url)
        print(json.dumps(res, indent=2))
    except Exception as e:
        import traceback
        traceback.print_exc()

test()
