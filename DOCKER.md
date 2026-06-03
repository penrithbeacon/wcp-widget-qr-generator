# WCP Widget: QR Generator

A [Widget Context Protocol (WCP)](https://widgetcontextprotocol.com) compliant widget that
generates QR codes for any text or URL. Fully self-contained — no external API calls, works
offline. Designed to run alongside any WCP-compatible host dashboard.

**Specification:** [widgetcontextprotocol.com](https://widgetcontextprotocol.com)

## Quick Start

```bash
docker run -d \
  --name wcp-widget-qr-generator \
  -p 3738:3738 \
  --restart unless-stopped \
  penrithbeacon/wcp-widget-qr-generator:latest
```

Then add it to your WCP dashboard at the container's network address.

## Docker Compose

```yaml
services:
  qr-generator:
    image: penrithbeacon/wcp-widget-qr-generator:latest
    container_name: wcp-widget-qr-generator
    ports:
      - "3738:3738"
    restart: unless-stopped
```

## WCP Request Headers

This widget supports the WCP 1.5.0 request headers:

| Header | Required | Description |
|--------|----------|-------------|
| `Wcp-Instance-Id` | Required | UUID identifying this widget instance |
| `Wcp-Dashboard-Id` | Optional | UUID identifying the requesting dashboard |
| `Wcp-Version` | Optional | Protocol version the dashboard speaks |
| `Wcp-Widget-Id` | Optional | Widget ID from Container Directory selection |
| `Wcp-Orchestration-Id` | Optional | UUID of the active orchestration — shared state key for multi-component coordination |
| `Wcp-Application-Id` | Optional | UUID of the active application window (kiosk only) — combined with orchestration ID for full isolation |

## WCP Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /wcp` | WCP 1.5.0 Container Directory |
| `GET /widget/` | Compact widget view (iframe) |
| `GET /widget/wcp` | WCP 1.5.0 manifest |
| `GET /widget/health` | Health check |
| `GET /widget/icon.svg` | Widget icon (SVG) |
| `GET /widget/full` | Full-page QR generator |
| `GET /widget/api/guids` | Server and component UUIDs for Bonjour discovery |
| `POST /widget/api/qr` | Generate a QR code |

## API

**Generate a QR code:**
```bash
curl -X POST http://192.168.1.42:3738/widget/api/qr \
  -H "Content-Type: application/json" \
  -d '{"text": "https://example.com", "size": 300}'
```

Response:
```json
{
  "status": "Success",
  "text": "https://example.com",
  "size": 300,
  "format": "png",
  "base64Image": "<base64-encoded PNG>"
}
```

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `text` | string | required | Text or URL to encode |
| `size` | integer | 300 | Output image size in pixels (50–2000) |

## WCP Compatibility

| Property | Value |
|----------|-------|
| WCP Version | 1.5.0 |
| Widget Version | 1.2.1 |
| Render mode | iframe |
| Auth | none |
| Default card size | 4×3 |
| Multi-instance | Stateless — no configuration stored |

## Technical Details

- **Base image:** `python:3.12-slim`
- **Port:** `3738`
- **Dependencies:** Flask, qrcode, Pillow
- **No external API calls** — fully self-contained, works offline
- **No persistent storage required** — stateless

## Tags

| Tag | Description |
|-----|-------------|
| `latest` | Latest stable release |
| `1.2.1-wcp1.4.0` | Widget v1.2.1, WCP 1.5.0 — server UUID, Container Directory, Wcp-Widget-Id |
| `1.2.0-wcp1.3.1` | Widget v1.2.0, WCP 1.3.1 — CORS headers, multi-instance support |
| `1.1.0-wcp1.3.0` | Widget v1.1.0, WCP 1.3.0 — mandatory components array |

## Source

- Docker Hub: [penrithbeacon/wcp-widget-qr-generator](https://hub.docker.com/r/penrithbeacon/wcp-widget-qr-generator)
- GitHub: [penrithbeacon/wcp-widget-qr-generator](https://github.com/penrithbeacon/wcp-widget-qr-generator)
- WCP Specification: [widgetcontextprotocol.com](https://widgetcontextprotocol.com)
