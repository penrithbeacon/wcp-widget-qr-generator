"""
WCP Widget: QR Generator
Widget Context Protocol 2.0.0 compliant
Port: 3738  |  Specification: https://widgetcontextprotocol.com
"""

import io
import base64
import json
import os
import zipfile
from flask import Flask, render_template, jsonify, request, Response

try:
    import qrcode
    from PIL import Image
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

app = Flask(__name__)

PUBLISHED_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'published', 'index.html')

# ── CORS ──────────────────────────────────────────────────────────────────────

@app.after_request
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin']  = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = (
        'Content-Type, Wcp-Instance-Id, Wcp-Dashboard-Id, Wcp-Version, Wcp-Widget-Id, '
        'Wcp-Orchestration-Id, Wcp-Application-Id'
    )
    return response

@app.route('/widget/<path:p>', methods=['OPTIONS'])
@app.route('/widget/', methods=['OPTIONS'])
@app.route('/wcp', methods=['OPTIONS'])
def cors_preflight(p=''):
    return Response('', status=204)

# ── Instance ID helper ────────────────────────────────────────────────────────

def get_instance_id():
    iid = request.headers.get("Wcp-Instance-Id", "").strip()
    if not iid:
        iid = (request.args.get("wcpInstanceId", "") or "").strip()
    return iid

def get_orchestration_id():
    oid = request.headers.get("Wcp-Orchestration-Id", "").strip()
    if not oid:
        oid = (request.args.get("wcpOrchestrationId", "") or "").strip()
    return oid

def get_application_id():
    aid = request.headers.get("Wcp-Application-Id", "").strip()
    if not aid:
        aid = (request.args.get("wcpApplicationId", "") or "").strip()
    return aid

def get_state_key():
    """WCP 1.5.0 compound state key. See widgetcontextprotocol.com — WCP Request Headers."""
    orch_id = get_orchestration_id()
    app_id  = get_application_id()
    if orch_id and app_id: return f"{orch_id}:{app_id}"
    if orch_id:            return orch_id
    return "global"

# ── WCP Manifest ─────────────────────────────────────────────────────────────

WCP_MANIFEST = {
    "wcp": "2.1.0",
    "uuid": "657a538f-54b4-4315-b624-8304b5c69865",
    "name": "QR Generator",
    "version": "1.8.0",
    "description": (
        "Generate QR codes for any text or URL. "
        "Standalone — no external dependencies required."
    ),
    "icon": "/widget/icon.svg",
    "health": "/widget/health",
    "container": {
        "image":            "docker.io/penrithbeacon/wcp-widget-qr-generator",
        "source":           {"type": "registry"},
        "tag":              "1.8.0-wcp2.1.0",
        "port":             3738,
        "defaultLifecycle": "always",
    },
    "components": [
        {
            "id": "qr-generator",
            "uuid": "9296f300-78b9-4c07-afbe-f2579bcc50fc",
            "name": "QR Generator",
            "role": "widget",
            "path": "/widget/",
            "icon": "/widget/icon.svg",
            "renderMode": "iframe",
            "defaultSize": {"w": 4, "h": 6},
        }
    ],
    "pages": [
        {
            "id": "full",
            "path": "/widget/full",
            "title": "QR Generator — Full Size",
            "description": "Generate large QR codes without size constraints.",
            "window": {"width": 820, "height": 620},
        }
    ],
    "actions": [
        {
            "id": "open-full-window",
            "type": "wcp:open-window",
            "label": "Open Full Screen",
            "page": "full",
        },
        {
            "id": "open-full-tab",
            "type": "wcp:open-tab",
            "label": "Open in New Tab",
            "page": "full",
            "tab": {"title": "QR Generator", "icon": "/widget/icon.svg"},
            "persist": False,
        },
    ],
}

# ── JSON-LD structured data ───────────────────────────────────────────────────

WIDGET_JSONLD = json.dumps({
    "@context": "https://schema.org",
    "@type": "SoftwareApplication",
    "name": WCP_MANIFEST["name"],
    "softwareVersion": WCP_MANIFEST["version"],
    "description": WCP_MANIFEST["description"],
    "identifier": WCP_MANIFEST["uuid"],
    "applicationCategory": "WCP Widget",
    "operatingSystem": "Web",
    "isBasedOn": {
        "@type": "WebSite",
        "name": "Widget Context Protocol",
        "url": "https://widgetcontextprotocol.com",
    },
    "additionalProperty": [
        {"@type": "PropertyValue", "name": "wcpVersion",      "value": WCP_MANIFEST["wcp"]},
        {"@type": "PropertyValue", "name": "containerImage",  "value": WCP_MANIFEST["container"]["image"]},
        {"@type": "PropertyValue", "name": "containerTag",    "value": WCP_MANIFEST["container"]["tag"]},
        {"@type": "PropertyValue", "name": "containerPort",   "value": str(WCP_MANIFEST["container"]["port"])},
    ],
}, indent=2)

# ── WCP endpoints ─────────────────────────────────────────────────────────────

@app.route("/wcp")
def container_directory():
    return jsonify({
        "type":    "directory",
        "wcp":     "2.1.0",
        "widgets": [{
            "id":          "qr-generator",
            "uuid":        WCP_MANIFEST["uuid"],
            "name":        WCP_MANIFEST["name"],
            "description": WCP_MANIFEST["description"],
            "icon":        WCP_MANIFEST["icon"],
            "manifest":    "/widget/wcp",
        }]
    })

@app.route('/')
def published_spa():
    if os.path.exists(PUBLISHED_PATH):
        with open(PUBLISHED_PATH, 'r', encoding='utf-8') as f:
            return Response(f.read(), mimetype='text/html')
    return Response('Not Found', status=404, mimetype='text/plain')

@app.route('/widget/publish', methods=['POST'])
def publish():
    html = request.get_data(as_text=True)
    if not html:
        return jsonify({'success': False, 'error': 'Empty body'}), 400
    try:
        os.makedirs(os.path.dirname(PUBLISHED_PATH), exist_ok=True)
        with open(PUBLISHED_PATH, 'w', encoding='utf-8') as f:
            f.write(html)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/widget/publish', methods=['DELETE'])
def unpublish():
    try:
        if os.path.exists(PUBLISHED_PATH):
            os.remove(PUBLISHED_PATH)
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route("/widget/")
@app.route("/widget/index.html")
def widget_compact():
    return render_template("widget.html", manifest=WCP_MANIFEST, jsonld=WIDGET_JSONLD,
        wcp_instance_id=get_instance_id(),
        wcp_orchestration_id=get_orchestration_id(), wcp_application_id=get_application_id())

@app.route("/widget/wcp")
def widget_wcp():
    manifest = dict(WCP_MANIFEST)
    manifest['web'] = {'published': os.path.exists(PUBLISHED_PATH)}
    return jsonify(manifest)

@app.route("/widget/index")
def widget_index():
    return render_template("index-page.html", manifest=WCP_MANIFEST, jsonld=WIDGET_JSONLD,
        wcp_instance_id=get_instance_id(),
        wcp_orchestration_id=get_orchestration_id(), wcp_application_id=get_application_id())

@app.route("/widget/manifest")
def widget_manifest():
    """Simplified manifest for backward compatibility."""
    m = WCP_MANIFEST
    return jsonify({
        "wcp": m["wcp"], "name": m["name"], "version": m["version"],
        "description": m["description"], "icon": m["icon"],
        "health": m["health"], "components": m["components"],
    })

@app.route("/widget/health")
def widget_health():
    return jsonify({"status": "ok", "name": WCP_MANIFEST["name"],
                    "container": os.environ.get("CONTAINER_NAME", "unknown")})

@app.route("/widget/full")
def widget_full():
    return render_template("full.html", manifest=WCP_MANIFEST, jsonld=WIDGET_JSONLD,
        wcp_instance_id=get_instance_id(),
        wcp_orchestration_id=get_orchestration_id(), wcp_application_id=get_application_id())

ICON_SVG = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">
  <path fill="#f0883e" d="M0 0h7v7H0V0zm1 1v5h5V1H1zm1 1h3v3H2V2zM9 0h7v7H9V0zm1 1v5h5V1h-5zm1 1h3v3h-3V2zM0 9h7v7H0V9zm1 1v5h5v-5H1zm1 1h3v3H2v-3zm8-1h1v1h-1v-1zm2 0h1v1h-1v-1zm2 0h1v1h-1v-1zm-4 2h1v1h-1v-1zm2 0h1v1h-1v-1zm-2 2h1v1h-1v-1zm2-2h1v4h-1v-4zm2 0h1v1h-1v-1zm0 2h1v1h-1v-1zm0 2h1v1h-1v-1zm-4 0h1v1h-1v-1z"/>
</svg>"""

@app.route("/widget/icon.svg")
def widget_icon():
    return Response(ICON_SVG, mimetype="image/svg+xml")

@app.route("/widget/api/guids")
def api_guids():
    return jsonify({
        "uuid": WCP_MANIFEST["uuid"],
        "components": [
            {"id": c["id"], "uuid": c["uuid"], "name": c["name"]}
            for c in WCP_MANIFEST.get("components", [])
        ]
    })

@app.route("/widget/export.wcp")
def export_wcp():
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("manifest.json", json.dumps(WCP_MANIFEST, indent=2))
        z.writestr("icon.svg", ICON_SVG)
        z.writestr("DOCKER.md", f"""# {WCP_MANIFEST['name']} — WCP Container

## Pull
```
docker pull penrithbeacon/wcp-widget-qr-generator
```

## Run
```
docker compose up -d
```

Port: 3738 | Spec: https://widgetcontextprotocol.com
""")
    buf.seek(0)
    name = WCP_MANIFEST["name"].lower().replace(" ", "-")
    resp = Response(buf.read(), mimetype="application/zip")
    resp.headers["Content-Disposition"] = f'attachment; filename="{name}.wcp"'
    return resp

# ── QR generation API ─────────────────────────────────────────────────────────

@app.route("/widget/api/qr", methods=["POST"])
def generate_qr():
    if not QR_AVAILABLE:
        return jsonify({"status": "Error", "error": "qrcode library not installed"}), 500

    data = request.get_json(force=True) or {}
    text = str(data.get("text", "")).strip()
    size = max(50, min(int(data.get("size", 300)), 2000))

    if not text:
        return jsonify({"status": "Error", "error": "text is required"}), 400

    qr = qrcode.QRCode(box_size=10, border=2)
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")
    img = img.resize((size, size), Image.LANCZOS)

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()

    return jsonify({
        "status": "Success",
        "text": text,
        "size": size,
        "format": "png",
        "base64Image": b64,
    })

# ── Run ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=3738, debug=False)
