import urllib.request
import json

def get_json(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def test():
    try:
        events = get_json("http://127.0.0.1:8000/api/events/?limit=5")
        for e in events:
            print(f"[{e['timestamp']}] {e['type']} | User: {e.get('user_id')} | Cam: {e['camera_id']}")
            print(f"  Details: {e['details']}")
    except Exception as e:
        import traceback
        traceback.print_exc()

test()
