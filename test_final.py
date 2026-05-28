import urllib.request
import json

def post_json(url, data={}):
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'}, method="POST")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def get_json(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def test():
    # Set clock to Monday 08:30 (Morning Lab schedule)
    print("Setting clock to 2026-03-23 08:30...")
    print(post_json("http://127.0.0.1:8000/api/sim-clock/set", {"date": "2026-03-23", "hour": 8, "minute": 30}))
    
    # Knock on Telematics Lab
    print("\nKnocking on Telematics Lab (qIH3ae0D99tTU5diycoG)...")
    res = post_json("http://127.0.0.1:8000/api/doors/qIH3ae0D99tTU5diycoG/knock")
    print(res)

test()
