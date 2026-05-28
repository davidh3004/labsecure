/* Dashboard.tsx — Live Security Feed */

import { useState, useEffect, useRef } from 'react';
import { VideoOff, Activity } from 'lucide-react';
import { camerasApi, createFeedSocket } from '../api/client';
import type { CameraConfig } from '../api/types';

interface FeedState {
    connected: boolean;
    hasFrame: boolean;
    fps: number;
}

/* ── CameraFeed ─────────────────────────────────────────────────────────────
 * Renders a live JPEG stream from the backend pipeline.
 *
 * Strategy: canvas + off-screen Image decode
 *   - Each incoming JPEG (snapshot or WebSocket binary frame) is decoded by a
 *     throwaway Image object. When it finishes loading (onload), we drawImage
 *     onto the canvas and immediately revoke the blob URL.
 *   - Canvas always paints whatever was last drawn — no React state involved
 *     in the pixel data, no Safari blob-revoke timing issues, no React
 *     reconciliation touching the element between frames.
 *   - frameSeqRef ensures that if a newer frame arrives while an older one is
 *     still decoding, the older draw is silently discarded.
 * ─────────────────────────────────────────────────────────────────────────── */
function CameraFeed({ camera }: { camera: CameraConfig }) {
    const [state, setState] = useState<FeedState>({ connected: false, hasFrame: false, fps: 0 });
    const wsRef = useRef<WebSocket | null>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const frameCountRef = useRef(0);
    const fpsTimerRef = useRef<ReturnType<typeof setInterval>>();
    const frameSeqRef = useRef(0);

    useEffect(() => {
        let destroyed = false;

        const drawFrame = (blob: Blob) => {
            const canvas = canvasRef.current;
            if (!canvas || destroyed) return;

            // Tag this decode with a sequence number. If a newer frame arrives
            // before this one finishes decoding, this draw becomes a no-op.
            const seq = ++frameSeqRef.current;
            const url = URL.createObjectURL(blob);
            const img = new Image();

            img.onload = () => {
                // Always revoke immediately — image data is in browser memory now
                URL.revokeObjectURL(url);
                if (frameSeqRef.current !== seq || destroyed) return;

                const ctx = canvas.getContext('2d');
                if (!ctx) return;

                // Resize canvas intrinsic dimensions only when they change
                if (canvas.width !== img.naturalWidth || canvas.height !== img.naturalHeight) {
                    canvas.width = img.naturalWidth;
                    canvas.height = img.naturalHeight;
                }
                ctx.drawImage(img, 0, 0);

                if (!destroyed) setState(s => s.hasFrame ? s : { ...s, hasFrame: true });
            };

            img.onerror = () => URL.revokeObjectURL(url);
            img.src = url;
        };

        // Snapshot: paint the first frame before WS connects
        const API_BASE = import.meta.env.VITE_API_BASE || '';
        fetch(`${API_BASE}/api/cameras/${camera.id}/snapshot`)
            .then(r => r.ok ? r.blob() : null)
            .then(blob => { if (blob && !destroyed) drawFrame(blob); })
            .catch(() => {});

        // WebSocket: continuous annotated JPEG stream
        const connect = () => {
            if (destroyed) return;
            try {
                const ws = createFeedSocket(camera.id);
                ws.binaryType = 'arraybuffer';
                wsRef.current = ws;

                ws.onopen = () => setState(s => ({ ...s, connected: true }));

                ws.onmessage = (event) => {
                    if (event.data instanceof ArrayBuffer) {
                        drawFrame(new Blob([event.data], { type: 'image/jpeg' }));
                        frameCountRef.current++;
                    } else if (event.data instanceof Blob) {
                        // Fallback: some environments deliver binary as Blob
                        // even when binaryType = 'arraybuffer'
                        drawFrame(event.data);
                        frameCountRef.current++;
                    }
                };

                ws.onerror = () => setState(s => ({ ...s, connected: false }));
                ws.onclose = () => {
                    setState(s => ({ ...s, connected: false }));
                    if (!destroyed) setTimeout(connect, 3000);
                };
            } catch {
                if (!destroyed) setTimeout(connect, 3000);
            }
        };

        connect();

        fpsTimerRef.current = setInterval(() => {
            setState(s => ({ ...s, fps: frameCountRef.current }));
            frameCountRef.current = 0;
        }, 1000);

        return () => {
            destroyed = true;
            wsRef.current?.close();
            clearInterval(fpsTimerRef.current);
        };
    }, [camera.id]);

    return (
        <div className="feed-panel">
            <div className="feed-header">
                <div className="feed-camera-name">
                    <span className={`status-dot ${state.connected ? 'online' : 'offline'}`} />
                    {camera.name}
                </div>
                <div className="feed-stats">
                    <span><Activity size={12} /> {state.fps} FPS</span>
                    <span className={`badge ${state.connected ? 'badge-success' : 'badge-danger'}`}>
                        {state.connected ? 'LIVE' : 'OFFLINE'}
                    </span>
                </div>
            </div>
            <div className="feed-canvas">
                <canvas
                    ref={canvasRef}
                    style={{ display: state.hasFrame ? 'block' : 'none' }}
                />
                {!state.hasFrame && (
                    <div className="feed-offline">
                        <VideoOff size={40} />
                        <span>{state.connected ? 'Waiting for frames...' : 'Camera offline'}</span>
                    </div>
                )}
            </div>
        </div>
    );
}

export default function Dashboard() {
    const [cameras, setCameras] = useState<CameraConfig[]>([]);

    useEffect(() => {
        camerasApi.list().then(setCameras).catch(() => setCameras([]));
    }, []);

    const enabledCameras = cameras.filter(c => c.enabled);

    return (
        <div>
            {enabledCameras.length === 0 ? (
                <div className="card" style={{ textAlign: 'center', padding: '100px 20px' }}>
                    <VideoOff size={56} style={{ color: 'var(--text-tertiary)', margin: '0 auto 16px' }} />
                    <div style={{ color: 'var(--text-secondary)', fontWeight: 600, fontSize: 18, marginBottom: 8 }}>
                        No cameras configured
                    </div>
                    <div style={{ color: 'var(--text-tertiary)', fontSize: 14 }}>
                        Go to <strong>Camera Health</strong> to add your webcam or IP cameras
                    </div>
                </div>
            ) : (
                <div className="feed-grid">
                    {enabledCameras.map(cam => <CameraFeed key={cam.id} camera={cam} />)}
                </div>
            )}
        </div>
    );
}
