import urllib.request
import json
import traceback

def get_json(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def post_json(url, data={}):
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'}, method="POST")
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def test():
    try:
        health = get_json("http://127.0.0.1:8000/health")
        print("Health:", health)
        
        sim = get_json("http://127.0.0.1:8000/api/sim-clock/")
        print("Sim Clock:", sim)
        
        cams = get_json("http://127.0.0.1:8000/api/cameras/list")
        if not cams:
            print("No cameras")
        else:
            for c in cams:
                print("Camera", c)
                
        rooms = get_json("http://127.0.0.1:8000/api/rooms")
        for r in rooms:
            if r['name'] == 'Telematics Lab':
                print("\nKnocking on Telematics Lab...")
                res = post_json(f"http://127.0.0.1:8000/api/doors/{r['id']}/knock")
                print(res)
    except Exception as e:
        traceback.print_exc()

test()
