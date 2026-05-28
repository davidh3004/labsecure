import urllib.request
import json
import traceback

def get_json(url):
    req = urllib.request.Request(url)
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())

def test():
    try:
        from backend.dependencies import vision_pipeline
        print("This runs in a different process, so I can't access vision_pipeline memory.")
    except Exception as e:
        pass

test()
