from flask import Flask, render_template, jsonify, request
from scraper import fetch_all_updates, load_updates
from ai_agent import process_updates, generate_digest
from apscheduler.schedulers.background import BackgroundScheduler
import json
import atexit

app = Flask(__name__)

# ─── Auto-run scraper + AI every 24 hours ─────────────────────────────────────
scheduler = BackgroundScheduler()

def scheduled_job():
    print("⏰ Scheduled job running...")
    fetch_all_updates()
    process_updates()

if not scheduler.running:
    scheduler.add_job(scheduled_job, 'interval', hours=24)
    scheduler.start()

atexit.register(lambda: scheduler.shutdown(wait=False))

# ─── Home Dashboard ───────────────────────────────────────────────────────────
@app.route("/")
def index():
    return render_template("index.html")

# ─── API: Get All Updates ─────────────────────────────────────────────────────
@app.route("/api/updates")
def get_updates():
    regulator = request.args.get("regulator", "ALL")
    impact = request.args.get("impact", "ALL")
    updates = load_updates()
    if regulator != "ALL":
        updates = [u for u in updates if u.get("regulator") == regulator]
    if impact != "ALL":
        updates = [u for u in updates if u.get("impact") == impact]
    return jsonify(updates)

# ─── API: Get Stats ───────────────────────────────────────────────────────────
@app.route("/api/stats")
def get_stats():
    updates = load_updates()
    stats = {
        "total": len(updates),
        "rbi":   len([u for u in updates if u.get("regulator") == "RBI"]),
        "sebi":  len([u for u in updates if u.get("regulator") == "SEBI"]),
        "irdai": len([u for u in updates if u.get("regulator") == "IRDAI"]),
        "high":  len([u for u in updates if u.get("impact") == "High"]),
        "medium":len([u for u in updates if u.get("impact") == "Medium"]),
        "low":   len([u for u in updates if u.get("impact") == "Low"]),
    }
    return jsonify(stats)

# ─── API: Refresh Updates ─────────────────────────────────────────────────────
@app.route("/api/refresh", methods=["POST"])
def refresh():
    fetch_all_updates()
    process_updates()
    return jsonify({"status": "success", "message": "Updates refreshed!"})

# ─── API: Get Digest ──────────────────────────────────────────────────────────
@app.route("/api/digest")
def get_digest():
    updates = load_updates()
    digest = generate_digest(updates)
    return jsonify({"digest": digest})

# ─── Run App ──────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    print("🚀 Regulatory Watch Agent Starting...")
    print("📊 Dashboard: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)
