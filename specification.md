# QR Generator — Specification

## Overview
Generate QR codes for any text or URL. Standalone — no external dependencies required.

- **Port:** 3738
- **Container:** `wcp-widget-qr-generator`
- **Image:** `docker.io/penrithbeacon/wcp-widget-qr-generator`

## Version
- **Widget:** 1.8.0
- **WCP:** 2.1.0
- **Docker tag:** `1.8.0-wcp2.1.0`

## Controls (HTML Templates)

| Template | Route | Purpose | Default Size |
|----------|-------|---------|--------------|
| widget.html | `/widget/` | Compact QR generator | 4×6 |
| full.html | `/widget/full` | Full-size QR generator | Window: 820×620 |

## API Endpoints

| Method | Route | Purpose |
|--------|-------|---------|
| GET | `/wcp` | Container directory |
| GET | `/widget/wcp` | Widget manifest |
| GET | `/widget/index` | Widget index directory |
| GET | `/widget/` | Compact view |
| GET | `/widget/full` | Full-page view |
| GET | `/widget/health` | Health check |
| GET | `/widget/icon.svg` | Widget icon |
| GET | `/widget/manifest` | Lightweight manifest subset |
| GET | `/widget/api/guids` | Component UUIDs |
| GET | `/widget/export.wcp` | WCP export package |
| POST | `/widget/api/qr` | Generate QR code |
| POST | `/widget/publish` | Publish SPA |
| DELETE | `/widget/publish` | Remove published SPA |
| GET | `/` | Serve published SPA |

## Features
- QR code generation for arbitrary text/URL
- Configurable size, error correction level, colours
- Download as PNG
- Full-page mode for large QR codes
- Publish to Web support

## Configuration
- No persistent configuration required
- All settings are per-session in the UI

## Data Persistence
- No data volume (stateless)
- Published SPA stored in `./published/` volume mount

## Dependencies
- Python: `flask`, `qrcode`, `Pillow`
- No external API dependencies
