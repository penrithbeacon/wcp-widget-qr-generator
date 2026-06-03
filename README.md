# WCP Widget — QR Generator

A [Widget Context Protocol (WCP)](https://widgetcontextprotocol.com) widget that generates
QR codes for any text or URL. Fully self-contained — no external API calls, works offline.

**Specification:** [widgetcontextprotocol.com](https://widgetcontextprotocol.com)  
**Part of the** [Penrith Beacon WCP](https://penrithbeacon.com) widget suite.

> **WCP 1.5.0 certified.** This widget implements the full
> [Widget Context Protocol 1.5.0](https://widgetcontextprotocol.com) specification,
> including server UUID, Container Directory (`GET /wcp`), all six `Wcp-*` request headers, and context-scoped runtime state isolation (`Wcp-Orchestration-Id`, `Wcp-Application-Id`).

---

## Components

| Component | Default size | What it shows |
|-----------|:------------:|---------------|
| **QR Generator** | 4 × 3 | QR code generator for any text or URL, with adjustable size |

---

## Requirements

- Docker and Docker Compose

No API keys or external services required — fully self-contained.

---

## Quick Start

```bash
docker run -d \
  --name wcp-widget-qr-generator \
  -p 3738:3738 \
  --restart unless-stopped \
  penrithbeacon/wcp-widget-qr-generator:latest
```

Then add it to your WCP dashboard at `http://localhost:3738`.

---

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

---

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

---

## Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `GET /wcp` | GET | WCP 1.5.0 Container Directory |
| `GET /widget/` | GET | Compact widget view (iframe) |
| `GET /widget/wcp` | GET | WCP 1.5.0 manifest |
| `GET /widget/health` | GET | `{"status":"ok","name":"QR Generator"}` |
| `GET /widget/icon.svg` | GET | Widget icon (SVG) |
| `GET /widget/full` | GET | Full-page QR generator |
| `GET /widget/api/guids` | GET | Server and component UUIDs for Bonjour discovery |
| `GET /widget/export.wcp` | GET | Self-export as a `.wcp` package |
| `POST /widget/api/qr` | POST | Generate a QR code |

---

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
| `size` | integer | 300 | Output size in pixels (50–2000) |

---

## Data Storage

This widget is **stateless** — it stores no configuration and requires no persistent volume.
Each QR code is generated on demand and returned in the response.

---

## WCP Compatibility

| Property | Value |
|----------|-------|
| WCP Version | 1.5.0 |
| Widget Version | 1.2.1 |
| Render mode | iframe |
| Auth | none |
| Default card size | 4 × 3 |
| Multi-instance | Stateless — no per-instance configuration |

---

## Technical Details

- **Base image:** `python:3.12-slim`
- **Port:** `3738`
- **Dependencies:** Flask, qrcode, Pillow
- **No external API calls** — fully self-contained, works offline
- **No persistent storage required** — stateless

---

## Links

- [Penrith Beacon](https://penrithbeacon.com)
- [Widget Context Protocol specification](https://widgetcontextprotocol.com)
- [Docker Hub — penrithbeacon/wcp-widget-qr-generator](https://hub.docker.com/r/penrithbeacon/wcp-widget-qr-generator)
