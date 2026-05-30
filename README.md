# wcp-widget-qr-generator

A WCP (Widget Context Protocol) compliant QR code generator widget.

## Port: 3738

## Quick Start

```bash
docker compose up --build
```

Widget available at: `http://localhost:3738/widget/`
WCP manifest at: `http://localhost:3738/widget/wcp`

## Development (no Docker)

```bash
pip install -r requirements.txt
cd src && python app.py
```

## WCP Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /widget/` | Compact widget iframe view |
| `GET /widget/wcp` | Full WCP 1.0.0 manifest |
| `GET /widget/manifest` | Simplified manifest |
| `GET /widget/health` | Health check |
| `GET /widget/full` | Full-page generator |
| `GET /widget/icon.svg` | Widget icon |
| `POST /widget/api/qr` | Generate QR: `{text, size}` → `{status, base64Image}` |
