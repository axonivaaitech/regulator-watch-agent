import anthropic
import json
import os
from scraper import load_updates, save_updates

import os

def get_client():
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    return anthropic.Anthropic(api_key=api_key)

# ─── Classify Impact Level ────────────────────────────────────────────────────
def classify_impact(title, summary):
    title_lower = title.lower()
    high_keywords = [
        "aml", "kyc", "fraud", "penalty", "mandatory", "compliance",
        "deadline", "enforcement", "ban", "suspension", "risk", "fincrime",
        "money laundering", "terrorist financing", "immediate", "urgent"
    ]
    low_keywords = [
        "calendar", "auction", "statistical", "bulletin",
        "supplement", "tender", "weekly", "monthly"
    ]
    for word in high_keywords:
        if word in title_lower:
            return "High"
    for word in low_keywords:
        if word in title_lower:
            return "Low"
    return "Medium"

# ─── Classify Banking Area ────────────────────────────────────────────────────
def classify_area(title):
    title_lower = title.lower()
    areas = {
        "KYC / AML": ["kyc", "aml", "know your customer", "money laundering", "cdd"],
        "Digital Banking": ["digital", "fintech", "upi", "payment", "mobile banking", "internet banking"],
        "Lending": ["loan", "lending", "credit", "nbfc", "microfinance", "priority sector"],
        "Securities": ["securities", "equity", "mutual fund", "stock", "derivative", "sebi"],
        "Insurance": ["insurance", "irdai", "premium", "policy", "claim"],
        "Fraud / FinCrime": ["fraud", "fincrime", "cybercrime", "scam", "phishing"],
        "Capital Markets": ["bond", "treasury", "gilt", "government securities", "borrowing"],
        "Banking Supervision": ["pca", "npa", "capital adequacy", "basel", "rwa"],
    }
    for area, keywords in areas.items():
        for keyword in keywords:
            if keyword in title_lower:
                return area
    return "General Banking"

# ─── Summarize Single Update Using Claude ─────────────────────────────────────
def summarize_update(update):
    print(f"  🤖 Summarizing: {update['title'][:60]}...")
    try:
        prompt = f"""You are a senior banking regulatory compliance expert at Infosys.

Analyze this Indian regulatory update and provide a structured response:

Regulator: {update['regulator']}
Title: {update['title']}

Respond in EXACTLY this format:

SUMMARY:
[2-3 sentences explaining what this regulation is about in simple terms]

IMPACT:
[1 sentence on the business impact for banks/financial institutions]

ACTION REQUIRED:
[1 specific action compliance teams must take]

URGENCY: [High / Medium / Low]"""
        client = get_client()
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=300,
            messages=[{"role": "user", "content": prompt}]
        )

        response_text = message.content[0].text

        # Parse the response
        summary = ""
        impact_text = ""
        action = ""
        urgency = "Medium"

        lines = response_text.split("\n")
        current_section = ""
        for line in lines:
            line = line.strip()
            if line.startswith("SUMMARY:"):
                current_section = "summary"
            elif line.startswith("IMPACT:"):
                current_section = "impact"
            elif line.startswith("ACTION REQUIRED:"):
                current_section = "action"
            elif line.startswith("URGENCY:"):
                urgency_line = line.replace("URGENCY:", "").strip()
                if "High" in urgency_line:
                    urgency = "High"
                elif "Low" in urgency_line:
                    urgency = "Low"
                else:
                    urgency = "Medium"
            elif line and current_section == "summary":
                summary += line + " "
            elif line and current_section == "impact":
                impact_text += line + " "
            elif line and current_section == "action":
                action += line + " "

        return {
            "summary": summary.strip() or "AI summary not available.",
            "impact_text": impact_text.strip() or "Review required.",
            "action": action.strip() or "Monitor and assess.",
            "impact": urgency
        }

    except Exception as e:
        print(f"  ❌ AI Error: {e}")
        return {
            "summary": "Unable to generate AI summary at this time.",
            "impact_text": "Manual review required.",
            "action": "Please review the original document.",
            "impact": classify_impact(update["title"], "")
        }

# ─── Process all unsummarized updates ─────────────────────────────────────────
def process_updates():
    print("\n🤖 Starting AI Agent Processing...")
    print("=" * 50)

    updates = load_updates()
    processed_count = 0

    for i, update in enumerate(updates):
        # Only process if no summary yet
        if not update.get("summary"):
            print(f"\n[{i+1}/{len(updates)}] Processing {update['regulator']} update...")
            result = summarize_update(update)
            updates[i]["summary"] = result["summary"]
            updates[i]["impact_text"] = result.get("impact_text", "")
            updates[i]["action"] = result.get("action", "")
            updates[i]["impact"] = result["impact"]
            updates[i]["area"] = classify_area(update["title"])
            processed_count += 1

            # Save after each to avoid data loss
            save_updates(updates)

    print(f"\n✅ AI processing complete! {processed_count} updates summarized.")
    print("=" * 50)
    return updates

# ─── Generate Full Digest Summary ─────────────────────────────────────────────
def generate_digest(updates):
    print("\n📧 Generating daily digest...")
    try:
        high_impact = [u for u in updates if u.get("impact") == "High"]
        medium_impact = [u for u in updates if u.get("impact") == "Medium"]

        updates_text = ""
        for u in updates[:10]:
            updates_text += f"- [{u['regulator']}] {u['title'][:100]}\n"

        prompt = f"""You are a regulatory intelligence expert at Infosys FinCrime unit.

Create a professional daily regulatory digest email for Indian banking compliance teams.

Today's updates: {len(updates)} total
High impact: {len(high_impact)}
Medium impact: {len(medium_impact)}

Top updates:
{updates_text}

Write a professional 150-word executive summary starting with:
"📋 DAILY REGULATORY DIGEST - [Today's Date]"

Include:
1. Overall summary of today's updates
2. Key highlights (high impact items)
3. Recommended immediate actions
4. Sign off as: Regulatory Watch Agent | Powered by Axoniva AI Tech"""
        client = get_client()
        message = client.messages.create(
            model="claude-opus-4-5",
            max_tokens=400,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    except Exception as e:
        return f"Digest generation error: {e}"

# ─── Run directly ─────────────────────────────────────────────────────────────
if __name__ == "__main__":
    updates = process_updates()
    print("\n📧 Generating Digest...")
    digest = generate_digest(updates)
    print("\n" + digest)
