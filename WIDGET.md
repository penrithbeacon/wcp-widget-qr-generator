# QR Generator Widget — Specification

**Protocol:** WCP 1.0.0  
**Port:** 3738  
**Repo:** `wcp-widget-qr-generator` (private)  
**Tech:** Python 3.12 + Flask + qrcode[pil]

## What it does

Generates QR codes for any text or URL. Two views:
- **Compact** (`/widget/`) — fits inside a Pinboard card (max 400px QR)
- **Full page** (`/widget/full`) — no size limit, download button

## postMessage actions

The compact widget fires these when the user clicks the action buttons:

| Action | postMessage type | Opens |
|--------|-----------------|-------|
| "Full Screen" | `wcp:open-window` | New Electron window at `/widget/full` |
| "New Tab" | `wcp:open-tab` | New dashboard tab at `/widget/full` |

## QR API

`POST /widget/api/qr`

Request: `{ "text": "https://example.com", "size": 300 }`  
Response: `{ "status": "Success", "text": "...", "size": 300, "format": "png", "base64Image": "..." }`

Size is clamped to 50–400px in compact view, 50–2000px in full-page view.

## Upgrading

```bash
# Bump version in app.py (WCP_MANIFEST["version"])
# Rebuild Docker image
docker compose up --build -d
```
