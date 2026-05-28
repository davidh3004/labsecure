import urllib.request
import json
import sys

def get_json(url, method="GET"):
    req = urllib.request.Request(url, method=method)
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        print(f"Error {method} {url}: {e}")
        return None

def test():
    print("Health:", get_json("http://127.0.0.1:8000/health"))
    
    rooms = get_json("http://127.0.0.1:8000/api/rooms")
    if not rooms:
        print("No rooms found or API error")
        return
        
    for r in rooms:
        rid = r.get("id")
        print(f"\nKnocking on room {r.get('name')} ({rid})...")
        res = get_json(f"http://127.0.0.1:8000/api/doors/{rid}/knock", method="POST")
        print(res)
        
    cams = get_json("http://127.0.0.1:8000/api/cameras")
    print("\nCameras:")
    print(cams)

test()
