import urllib.request
import json

def get_json(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def test():
    try:
        events = get_json("http://127.0.0.1:8000/api/events/?limit=10")
        for e in events:
            if e['type'] == 'unknown_face':
                print(f"[{e['timestamp']}] UNKNOWN | Confidence: {e['details'].get('confidence')}")
            else:
                print(f"[{e['timestamp']}] {e['type']} | Conf: {e['details'].get('confidence')}")
    except Exception as e:
        import traceback
        traceback.print_exc()

test()
