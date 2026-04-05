import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# ─── Data file path ───────────────────────────────────────────────────────────
DATA_FILE = "data/updates.json"

# ─── Load existing updates ────────────────────────────────────────────────────
def load_updates():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# ─── Save updates ─────────────────────────────────────────────────────────────
def save_updates(updates):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)  # ← ADD THIS LINE
    with open(DATA_FILE, "w") as f:
        json.dump(updates, f, indent=2)

# ─── Scrape RBI ───────────────────────────────────────────────────────────────
def scrape_rbi():
    print("🔍 Scraping RBI...")
    results = []
    try:
        url = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")

        # Find press release links
        links = soup.find_all("a", href=True)
        count = 0
        for link in links:
            text = link.get_text(strip=True)
            href = link["href"]
            if len(text) > 30 and count < 10:
                full_url = f"https://www.rbi.org.in{href}" if href.startswith("/") else href
                results.append({
                    "id": f"rbi_{hash(text) % 100000}",
                    "regulator": "RBI",
                    "title": text[:200],
                    "url": full_url,
                    "date": datetime.now().strftime("%d %b %Y"),
                    "summary": "",
                    "impact": "Medium",
                    "area": "Banking"
                })
                count += 1
        print(f"✅ RBI: Found {len(results)} updates")
    except Exception as e:
        print(f"❌ RBI scraping error: {e}")
        # Add sample data if scraping fails
        results = get_sample_rbi_data()
    return results

# ─── Scrape SEBI ──────────────────────────────────────────────────────────────
def scrape_sebi():
    print("🔍 Scraping SEBI...")
    results = []
    try:
        url = "https://www.sebi.gov.in/sebiweb/home/HomeAction.do?doListing=yes&sid=1&ssid=3&smid=0"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")

        rows = soup.find_all("td")
        count = 0
        for row in rows:
            text = row.get_text(strip=True)
            link_tag = row.find("a", href=True)
            if len(text) > 30 and link_tag and count < 10:
                href = link_tag["href"]
                full_url = f"https://www.sebi.gov.in{href}" if href.startswith("/") else href
                results.append({
                    "id": f"sebi_{hash(text) % 100000}",
                    "regulator": "SEBI",
                    "title": text[:200],
                    "url": full_url,
                    "date": datetime.now().strftime("%d %b %Y"),
                    "summary": "",
                    "impact": "Medium",
                    "area": "Securities"
                })
                count += 1
        print(f"✅ SEBI: Found {len(results)} updates")
    except Exception as e:
        print(f"❌ SEBI scraping error: {e}")
        results = get_sample_sebi_data()
    return results

# ─── Scrape IRDAI ─────────────────────────────────────────────────────────────
def scrape_irdai():
    print("🔍 Scraping IRDAI...")
    results = []
    try:
        url = "https://irdai.gov.in/web/guest/latest-news"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.content, "html.parser")

        links = soup.find_all("a", href=True)
        count = 0
        for link in links:
            text = link.get_text(strip=True)
            href = link["href"]
            if len(text) > 30 and count < 10:
                full_url = f"https://irdai.gov.in{href}" if href.startswith("/") else href
                results.append({
                    "id": f"irdai_{hash(text) % 100000}",
                    "regulator": "IRDAI",
                    "title": text[:200],
                    "url": full_url,
                    "date": datetime.now().strftime("%d %b %Y"),
                    "summary": "",
                    "impact": "Medium",
                    "area": "Insurance"
                })
                count += 1
        print(f"✅ IRDAI: Found {len(results)} updates")
    except Exception as e:
        print(f"❌ IRDAI scraping error: {e}")
        results = get_sample_irdai_data()
    return results

# ─── Sample Data (fallback if websites block scraping) ────────────────────────
def get_sample_rbi_data():
    return [
        {
            "id": "rbi_001",
            "regulator": "RBI",
            "title": "RBI releases guidelines on Digital Lending - Updated Framework for NBFCs and Banks",
            "url": "https://www.rbi.org.in",
            "date": datetime.now().strftime("%d %b %Y"),
            "summary": "",
            "impact": "High",
            "area": "Digital Lending"
        },
        {
            "id": "rbi_002",
            "regulator": "RBI",
            "title": "Master Direction on KYC - Amendments to Customer Due Diligence Requirements",
            "url": "https://www.rbi.org.in",
            "date": datetime.now().strftime("%d %b %Y"),
            "summary": "",
            "impact": "High",
            "area": "KYC / AML"
        },
        {
            "id": "rbi_003",
            "regulator": "RBI",
            "title": "Prompt Corrective Action Framework - Revised Thresholds for Banks",
            "url": "https://www.rbi.org.in",
            "date": datetime.now().strftime("%d %b %Y"),
            "summary": "",
            "impact": "Medium",
            "area": "Banking Supervision"
        }
    ]

def get_sample_sebi_data():
    return [
        {
            "id": "sebi_001",
            "regulator": "SEBI",
            "title": "SEBI circular on Alternative Investment Funds - New Compliance Requirements",
            "url": "https://www.sebi.gov.in",
            "date": datetime.now().strftime("%d %b %Y"),
            "summary": "",
            "impact": "High",
            "area": "Investment Funds"
        },
        {
            "id": "sebi_002",
            "regulator": "SEBI",
            "title": "Insider Trading Regulations - Amendment to Disclosure Requirements",
            "url": "https://www.sebi.gov.in",
            "date": datetime.now().strftime("%d %b %Y"),
            "summary": "",
            "impact": "Medium",
            "area": "Securities Trading"
        }
    ]

def get_sample_irdai_data():
    return [
        {
            "id": "irdai_001",
            "regulator": "IRDAI",
            "title": "IRDAI guidelines on Health Insurance Products - Standardisation of Terminology",
            "url": "https://irdai.gov.in",
            "date": datetime.now().strftime("%d %b %Y"),
            "summary": "",
            "impact": "Medium",
            "area": "Health Insurance"
        },
        {
            "id": "irdai_002",
            "regulator": "IRDAI",
            "title": "Motor Insurance Framework - Updated Third Party Liability Coverage",
            "url": "https://irdai.gov.in",
            "date": datetime.now().strftime("%d %b %Y"),
            "summary": "",
            "impact": "Low",
            "area": "Motor Insurance"
        }
    ]

# ─── Main fetch function ──────────────────────────────────────────────────────
def fetch_all_updates():
    print("\n🚀 Starting Regulatory Watch Agent Scraper...")
    print("=" * 50)

    all_new = []
    existing = load_updates()
    existing_ids = {u["id"] for u in existing}

    # Scrape all regulators
    rbi_updates = scrape_rbi()
    sebi_updates = scrape_sebi()
    irdai_updates = scrape_irdai()

    all_fetched = rbi_updates + sebi_updates + irdai_updates

    # Only add new ones
    for update in all_fetched:
        if update["id"] not in existing_ids:
            all_new.append(update)

    if all_new:
        combined = all_new + existing
        save_updates(combined[:50])  # Keep latest 50
        print(f"\n✅ {len(all_new)} new updates saved!")
    else:
        print("\n✅ No new updates found.")

    print("=" * 50)
    return all_new

# ─── Run directly ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    fetch_all_updates()
    updates = load_updates()
    print(f"\n📊 Total updates in database: {len(updates)}")
    for u in updates[:5]:
        print(f"  [{u['regulator']}] {u['title'][:80]}...")
