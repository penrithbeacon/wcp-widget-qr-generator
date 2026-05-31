# WCP Widget: QR Generator

A [Widget Context Protocol (WCP)](https://github.com/penrithbeacon/wcp-widget-qr-generator)
compliant widget that generates QR codes for any text or URL. Designed to run as a
sidecar container alongside the **Penrith Beacon WCP Dashboard** or any other WCP-compatible
host dashboard.

## Quick Start

```bash
docker run -d \
  --name wcp-widget-qr-generator \
  -p 3738:3738 \
  --restart unless-stopped \
  penrithbeacon/wcp-widget-qr-generator:latest
```

Then add it to your WCP dashboard by pointing it at `http://localhost:3738`.

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

## WCP Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /widget/` | Compact widget view (iframe) |
| `GET /widget/wcp` | WCP manifest |
| `GET /widget/health` | Health check |
| `GET /widget/icon.svg` | Widget icon |
| `GET /widget/full` | Full-page QR generator |
| `POST /widget/api/qr` | Generate a QR code |

## API

**Generate a QR code:**
```bash
curl -X POST http://localhost:3738/widget/api/qr \
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
| WCP Version | 1.1.0 |
| Widget Version | 1.0.0 |
| Render mode | iframe |
| Auth | none |
| Default card size | 4×3 |

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
| `1.0.0-wcp1.1.0` | Widget v1.0.0, WCP protocol v1.1.0 |

## Source

- Docker Hub: [penrithbeacon/wcp-widget-qr-generator](https://hub.docker.com/r/penrithbeacon/wcp-widget-qr-generator)
- GitHub: [penrithbeacon/wcp-widget-qr-generator](https://github.com/penrithbeacon/wcp-widget-qr-generator)
- WCP Specification: [widgetcontextprotocol.com](https://widgetcontextprotocol.com)
