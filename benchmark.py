#!/usr/bin/env python3
"""
LabSecure AI v2 — Performance Benchmark
Measures FaceEngine inference time and JPEG encode time on this machine
to determine sustainable streaming FPS.

Usage:
    python benchmark.py
"""

import sys
import time
import numpy as np

sys.path.insert(0, ".")


def bench(label: str, fn, n: int = 20):
    # Warm up
    for _ in range(3):
        fn()
    times = []
    for _ in range(n):
        t0 = time.perf_counter()
        fn()
        times.append(time.perf_counter() - t0)
    avg = sum(times) / len(times)
    print(f"  {label:<45} avg={avg*1000:6.1f}ms  ({1/avg:5.1f} fps)")
    return avg


def main():
    print("\nLabSecure AI v2 — Performance Benchmark")
    print("=" * 60)

    # ── JPEG encode ────────────────────────────────────────────
    import cv2

    print("\n[1] JPEG encode speed (cv2.imencode)")
    resolutions = [
        ("1280×720  quality=80", (720, 1280)),
        ("1280×720  quality=60", (720, 1280)),
        (" 640×360  quality=60", (360, 640)),
        (" 480×270  quality=60", (270, 480)),
    ]
    frames = {res: np.random.randint(0, 255, (*res, 3), dtype=np.uint8) for _, res in resolutions}
    encode_times = {}
    for label, res in resolutions:
        q = 80 if "80" in label else 60
        f = frames[res]
        t = bench(label, lambda f=f, q=q: cv2.imencode(".jpg", f, [cv2.IMWRITE_JPEG_QUALITY, q]))
        encode_times[label] = t

    # ── FaceEngine inference ───────────────────────────────────
    print("\n[2] FaceEngine inference (InsightFace buffalo_sc @ det_size=320)")
    try:
        from backend.vision.face_engine import FaceEngine

        print("  Initializing… ", end="", flush=True)
        t0 = time.perf_counter()
        engine = FaceEngine(provider="cpu", model_name="buffalo_sc", det_size=320)
        engine.initialize()
        print(f"done ({(time.perf_counter()-t0)*1000:.0f}ms)\n")

        frame_640 = np.random.randint(0, 255, (360, 640, 3), dtype=np.uint8)
        frame_720 = np.random.randint(0, 255, (720, 1280, 3), dtype=np.uint8)

        inf_640 = bench("detect() on 640×360 frame", lambda: engine.detect(frame_640), n=10)
        inf_720 = bench("detect() on 1280×720 frame", lambda: engine.detect(frame_720), n=10)

    except Exception as e:
        print(f"  FaceEngine init failed: {e}")
        inf_640 = inf_720 = 0.0

    # ── Summary ────────────────────────────────────────────────
    print("\n[3] Sustainable streaming FPS (encode + detection budget)")
    target_ms = 1000 / 15  # 15fps = 66.7ms budget per frame
    enc_640_ms = encode_times.get(" 640×360  quality=60", 0) * 1000
    enc_720_ms = encode_times.get("1280×720  quality=80", 0) * 1000
    inf_ms     = inf_640 * 1000

    print(f"\n  Frame budget at 15fps:     {target_ms:.1f}ms")
    print(f"  JPEG encode (640×360@60):  {enc_640_ms:.1f}ms")
    print(f"  JPEG encode (1280×720@80): {enc_720_ms:.1f}ms")
    if inf_ms:
        print(f"  FaceEngine inference:      {inf_ms:.1f}ms (separate thread — does not block display)")

    total_display_ms = enc_640_ms
    headroom = target_ms - total_display_ms
    print(f"\n  Display thread total:      {total_display_ms:.1f}ms")
    print(f"  Headroom at 15fps:         {headroom:.1f}ms  ({'OK' if headroom > 5 else 'TIGHT' if headroom > 0 else 'OVER BUDGET'})")

    if inf_ms:
        det_fps = 1000 / (inf_ms + 80)  # +80ms sleep from pipeline.py
        print(f"  Detection thread rate:     ~{det_fps:.1f} detections/sec")

    print()


if __name__ == "__main__":
    main()
