from backend.utils.config import load_config

cfg = load_config()
print("Config cameras:")
for c in cfg.get('cameras', []):
    print(c)
