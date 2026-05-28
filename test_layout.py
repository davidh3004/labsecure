import urllib.request
import json

def get_json(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def test():
    rooms = get_json("http://127.0.0.1:8000/api/rooms")
    cams = get_json("http://127.0.0.1:8000/api/cameras")
    for r in rooms:
        print(f"Room: {r['name']} ({r['id']})")
    for c in cams:
        print(f"Camera: {c['name']} ({c['id']}) -> room: {c.get('room_id')}")

test()
