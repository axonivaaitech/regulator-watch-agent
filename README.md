# 🛡️ RegulatorWatch AI Agent

> **Autonomous Regulatory Intelligence for Indian Banking**
> 
> Built by **Soorej Ramesan** (Emp No: 1150493) | Infosys Banking FinCrime Delivery Unit  
> Powered by **Anthropic Claude AI** | Infosys TOPAZ Innovation

[![Live Demo](https://img.shields.io/badge/🟢_LIVE-regulatorwatch--agent.onrender.com-06D6A0?style=for-the-badge)](https://regulatorwatch-agent.onrender.com)
[![Python](https://img.shields.io/badge/Python-3.10+-00B4D8?style=for-the-badge&logo=python)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-3.1-FF6B35?style=for-the-badge&logo=flask)](https://flask.palletsprojects.com)
[![Claude AI](https://img.shields.io/badge/Claude-Anthropic_AI-EF476F?style=for-the-badge)](https://anthropic.com)

---

## 📋 Table of Contents

- [What is RegulatorWatch?](#what-is-regulatorwatch)
- [How It Works](#how-it-works)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Local Setup](#local-setup)
- [Environment Variables](#environment-variables)
- [API Endpoints](#api-endpoints)
- [Deployment](#deployment)
- [Roadmap](#roadmap)

---

## 🎯 What is RegulatorWatch?

RegulatorWatch is a **fully autonomous AI Agent** that monitors India's three major financial regulators — **RBI, SEBI, and IRDAI** — and delivers real-time compliance intelligence to banking teams.

### The Problem
Indian banking compliance teams spend **100+ hours per month** manually tracking regulatory circulars. A single missed update can result in penalties worth crores of rupees.

### The Solution
RegulatorWatch eliminates this entirely. It runs a **7-step autonomous cycle every 24 hours** — scraping, reading, summarising, classifying, and delivering regulatory intelligence with **zero human intervention**.

---

## ⚙️ How It Works

```
┌─────────────────────────────────────────────────────────┐
│               7-STEP AUTONOMOUS AGENT LOOP               │
├─────────────────────────────────────────────────────────┤
│  01 → MONITOR    Scrape RBI, SEBI, IRDAI websites       │
│  02 → DETECT     Identify NEW circulars via ID hash     │
│  03 → READ       Claude AI reads each circular          │
│  04 → CLASSIFY   Assign impact: High / Medium / Low     │
│  05 → ROUTE      Identify banking area affected         │
│  06 → DIGEST     Generate professional email summary    │
│  07 → PUBLISH    Update live web dashboard              │
└─────────────────────────────────────────────────────────┘
         ↑                                        |
         └──────────── Repeat every 24h ──────────┘
```

---

## ✅ Features

| Feature | Status |
|---------|--------|
| 🏛️ RBI circular scraping | ✅ Live |
| 📈 SEBI circular scraping | ✅ Live |
| 🔐 IRDAI notification scraping | ✅ Live |
| 🤖 Claude AI summarisation | ✅ Live |
| 🔴 Impact classification (High/Med/Low) | ✅ Live |
| 🏦 Banking area routing (AML/KYC/Treasury etc.) | ✅ Live |
| 📊 Live web dashboard | ✅ Live |
| 🔍 Filter by regulator & impact | ✅ Live |
| 📧 Daily AI digest | ✅ Live |
| ⏰ Auto-run every 24 hours | ✅ Live |
| 🌐 Cloud deployed | ✅ Live |

---

## 🛠️ Tech Stack

```
┌─────────────────────────────────────────────────────────┐
│  LAYER 1 — DATA          │  Python + BeautifulSoup4     │
│  Scraping Engine         │  Requests, JSON storage      │
├─────────────────────────────────────────────────────────┤
│  LAYER 2 — AI            │  Anthropic Claude API        │
│  Intelligence Brain      │  claude-opus-4-5 model       │
├─────────────────────────────────────────────────────────┤
│  LAYER 3 — APPLICATION   │  Python Flask REST API       │
│  Backend + Frontend      │  HTML + CSS + JavaScript     │
│                          │  APScheduler, Gunicorn       │
├─────────────────────────────────────────────────────────┤
│  HOSTING                 │  Render.com cloud platform   │
│  VERSION CONTROL         │  GitHub                      │
└─────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
regulator-watch-agent/
│
├── app.py                  # Flask app — API routes + scheduler
├── scraper.py              # Web scraper for RBI, SEBI, IRDAI
├── ai_agent.py             # Claude AI summarisation + classification
├── requirements.txt        # Python dependencies
│
├── templates/
│   └── index.html          # Live dashboard frontend
│
├── data/
│   └── updates.json        # Auto-generated database (gitignored)
│
└── README.md               # This file
```

---

## 🚀 Local Setup

### Prerequisites
- Python 3.10 or higher
- pip
- An Anthropic API key (get one at [console.anthropic.com](https://console.anthropic.com))

### Step 1 — Clone the repository

```bash
git clone https://github.com/axonivaaitech/regulator-watch-agent.git
cd regulator-watch-agent
```

### Step 2 — Create a virtual environment

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### Step 3 — Install dependencies

```bash
pip install -r requirements.txt
```

### Step 4 — Set your API key

```bash
# Windows (Command Prompt)
set ANTHROPIC_API_KEY=sk-ant-api03-your-key-here

# Windows (PowerShell)
$env:ANTHROPIC_API_KEY="sk-ant-api03-your-key-here"

# Mac / Linux
export ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
```

### Step 5 — Run the scraper to populate data

```bash
python scraper.py
```

### Step 6 — Process updates with AI

```bash
python ai_agent.py
```

### Step 7 — Start the web server

```bash
python app.py
```

### Step 8 — Open the dashboard

```
http://localhost:5000
```

---

## 🔑 Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ANTHROPIC_API_KEY` | ✅ Yes | Your Anthropic Claude API key |

> ⚠️ **Never commit your API key to GitHub.** Always use environment variables.

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/` | Live dashboard (HTML) |
| `GET` | `/api/updates` | All updates (JSON) |
| `GET` | `/api/updates?regulator=RBI` | Filter by regulator |
| `GET` | `/api/updates?impact=High` | Filter by impact level |
| `GET` | `/api/stats` | Count by regulator & impact |
| `POST` | `/api/refresh` | Trigger manual scrape + AI run |
| `GET` | `/api/digest` | Generate AI daily digest |

### Example API Response — `/api/updates`

```json
[
  {
    "id": "rbi_12345",
    "regulator": "RBI",
    "title": "Directions under Section 35A of the Banking Regulation Act",
    "url": "https://www.rbi.org.in/...",
    "date": "05 Apr 2026",
    "summary": "RBI has issued supervisory directions against cooperative banks...",
    "impact": "High",
    "area": "Banking Supervision",
    "action": "Review counterparty exposure immediately."
  }
]
```

---

## ☁️ Deployment on Render.com

### Step 1 — Push to GitHub
Make sure your latest code is pushed to GitHub.

### Step 2 — Create Render Web Service
1. Go to [render.com](https://render.com) → New → Web Service
2. Connect your GitHub repository
3. Set the following:

| Setting | Value |
|---------|-------|
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app` |
| **Python Version** | `3.10` |

### Step 3 — Add Environment Variable
In Render → Environment → Add:
```
ANTHROPIC_API_KEY = sk-ant-api03-your-key-here
```

### Step 4 — Deploy
Click **Manual Deploy** → Your app is live!

---

## 🗺️ Roadmap

| Phase | Timeline | Features |
|-------|----------|----------|
| **Phase 1** ✅ | Now — Live | RBI/SEBI/IRDAI scraping, Claude AI summaries, web dashboard, email digest |
| **Phase 2** | Q2 2026 | FIU-IND & MCA, WhatsApp alerts, PDF reports, role-based access |
| **Phase 3** | Q3–Q4 2026 | International regulators (FATF), MS Teams/Slack, audit trail |
| **Vision** | 2027+ | Agentic auto-remediation, Finacle/Temenos integration, multi-bank SaaS |

---

## 👤 Author

**Soorej Ramesan**  
Employee No: 1150493  
Infosys  

---

## 🤖 Powered By

- [Anthropic Claude AI](https://anthropic.com) — AI summarisation & classification
- [Infosys–Anthropic Partnership](https://www.infosys.com) — Enterprise AI collaboration

---

## 📄 Licence

This project was developed as part of the **Infosys TOPAZ Innovation Programme**.  
All rights reserved © Soorej Ramesan | Infosys 2026.

---

> *"Most AI projects are ideas. RegulatorWatch is already running."*  
> — Infosys TOPAZ Submission, April 2026
