"""
WCP Widget: QR Generator
Widget Context Protocol 1.0.0 reference implementation
Port: 3738
"""

import io
import base64
import json
from flask import Flask, render_template, jsonify, request, Response

try:
    import qrcode
    from PIL import Image
    QR_AVAILABLE = True
except ImportError:
    QR_AVAILABLE = False

app = Flask(__name__)

# ── WCP Manifest ─────────────────────────────────────────────────────────────

WCP_MANIFEST = {
    "wcp": "1.3.0",
    "name": "QR Generator",
    "version": "1.1.0",
    "description": (
        "Generate QR codes for any text or URL. "
        "Standalone — no external dependencies required."
    ),
    "icon": "/widget/icon.svg",
    "health": "/widget/health",
    "components": [
        {
            "id": "qr-generator",
            "uuid": "9296f300-78b9-4c07-afbe-f2579bcc50fc",
            "name": "QR Generator",
            "role": "widget",
            "path": "/widget/",
            "icon": "/widget/icon.svg",
            "renderMode": "iframe",
            "defaultSize": {"w": 4, "h": 3},
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

# ── WCP endpoints ─────────────────────────────────────────────────────────────

@app.route("/widget/")
@app.route("/widget/index.html")
def widget_compact():
    return render_template("widget.html", manifest=WCP_MANIFEST)

@app.route("/widget/wcp")
def widget_wcp():
    return jsonify(WCP_MANIFEST)

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
    return jsonify({"status": "ok", "name": WCP_MANIFEST["name"]})

@app.route("/widget/full")
def widget_full():
    return render_template("full.html", manifest=WCP_MANIFEST)

@app.route("/widget/icon.svg")
def widget_icon():
    svg = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 16">
  <path fill="#f0883e" d="M0 0h7v7H0V0zm1 1v5h5V1H1zm1 1h3v3H2V2zM9 0h7v7H9V0zm1 1v5h5V1h-5zm1 1h3v3h-3V2zM0 9h7v7H0V9zm1 1v5h5v-5H1zm1 1h3v3H2v-3zm8-1h1v1h-1v-1zm2 0h1v1h-1v-1zm2 0h1v1h-1v-1zm-4 2h1v1h-1v-1zm2 0h1v1h-1v-1zm-2 2h1v1h-1v-1zm2-2h1v4h-1v-4zm2 0h1v1h-1v-1zm0 2h1v1h-1v-1zm0 2h1v1h-1v-1zm-4 0h1v1h-1v-1z"/>
</svg>"""
    return Response(svg, mimetype="image/svg+xml")

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
