import urllib.request
import json

def post_json(url, data={}):
    req = urllib.request.Request(url, data=json.dumps(data).encode(), headers={'Content-Type': 'application/json'}, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode())
    except Exception as e:
        return f"Error: {e}"

def get_json(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def test():
    schedules = get_json("http://127.0.0.1:8000/api/schedules")
    if not schedules:
        print("No schedules found")
        return
        
    sch = schedules[0]
    day = sch["days"][0]
    hour, minute = map(int, sch["start_time"].split(':'))
    print(f"Setting clock to {day} {hour}:{minute}")
    print(post_json("http://127.0.0.1:8000/api/sim-clock/set", {"day": day, "hour": hour, "minute": minute}))
    
    print(f"\nKnocking on {sch['room_id']} for schedule {sch['name']}...")
    res = post_json(f"http://127.0.0.1:8000/api/doors/{sch['room_id']}/knock")
    print("Knock Result:", res)

test()
