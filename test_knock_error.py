import urllib.request
import json
import traceback

def post_json(url, data={}):
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'}, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode()), response.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode()), e.code

def test():
    try:
        print("Setting clock to 2026-03-23 08:30...")
        post_json("http://127.0.0.1:8000/api/sim-clock/set", {"date": "2026-03-23", "hour": 8, "minute": 30})
        
        print("\nKnocking on Telematics Lab (qIH3ae0D99tTU5diycoG)...")
        res, status = post_json("http://127.0.0.1:8000/api/doors/qIH3ae0D99tTU5diycoG/knock")
        print(f"Status: {status}")
        print("Response:", res)
    except Exception as e:
        traceback.print_exc()

test()
