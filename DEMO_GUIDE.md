# Demo Guide - HomeLight RevOps MVP

## 🎯 What This Project Demonstrates

This project showcases my ability to:
- **Identify and solve real business problems** in revenue operations
- **Build end-to-end data products** from CSV to interactive dashboard
- **Design intuitive UIs** that non-technical users can adopt immediately
- **Integrate with external APIs** (Gmail API for draft creation)
- **Think like a product manager** while executing as an engineer

---

## 💼 Business Context

**Problem:** Revenue operations teams at companies like HomeLight struggle with:
- Tracking referral commissions across hundreds of deals
- Identifying which agents/partners are behind on payments
- Following up on overdue invoices consistently
- Prioritizing collection efforts by risk/amount

**Solution:** A real-time dashboard that:
1. **Surfaces risk** before it becomes a problem
2. **Prioritizes action** by agent and dollar amount  
3. **Automates outreach** with template-based emails
4. **Integrates with existing workflows** (Gmail)

---

## ✨ Key Features Built

### 1. **Referral-to-Revenue Scorecard**
- Top-line KPIs: Volume, Conversion %, Outstanding $, Avg Aging
- Real-time calculations from CSV data
- Clean, executive-friendly visualization

### 2. **Agent Risk Summary** (My Innovation!)
- Aggregates risk by agent/partner instead of by deal
- Priority flags: 🔴 High / 🟡 Medium / 🟢 Normal
- **Repeat offender detection**: +1 risk score if agent has 2+ at-risk deals
- **Business value**: Shifts focus from "which deal" to "which partner" - much more actionable

### 3. **Smart Email Generator**
- Auto-selects appropriate template based on days outstanding:
  - 7-14 days: Friendly reminder
  - 15-30 days: Value-oriented check-in
  - 30-45 days: Clear next step
  - 45+ days: Escalation with attachments
- Pre-fills all merge fields (agent name, client, amounts, dates)
- Ready-to-send emails in < 10 seconds

### 4. **Gmail Draft Integration** (Technical Highlight!)
- OAuth 2.0 authentication with Google
- One-click draft creation in user's Gmail
- Drafts appear in Gmail → Drafts for review before sending
- **Why drafts vs direct send**: Collections requires human judgment; this augments, doesn't replace

### 5. **Referral Client Database**
- **Search functionality**: Filter by client, agent, or referral ID
- **Rich client profiles**: Timeline, metrics, recommended next action
- **Smart recommendations**: "Send invoice today" vs "Escalation email + call"

### 6. **Data Quality & Logic**
- QA'd all data for:
  - Date consistency (referral → close → invoice → touch)
  - Commission calculations (price × rate)
  - Business logic (no commission for non-closed deals)
- Risk scoring is explainable (no black-box ML)

---

## 🔧 Technical Highlights

**Stack:**
- **Frontend**: Streamlit (rapid prototyping, but production-ready UI)
- **Data**: Pandas for ETL + feature engineering
- **API**: Google Gmail API with OAuth 2.0
- **Deployment-ready**: Requirements.txt, environment config, .gitignore

**Code Quality:**
- Modular functions (separation of concerns)
- Error handling for edge cases (NaN values, missing data)
- Documented setup process
- Git-ready with proper .gitignore

---

## 📊 Metrics That Matter

**Time saved:**
- Manual email drafting: ~5 min per email → ~30 seconds
- Finding at-risk accounts: ~15 min of spreadsheet work → instant

**Risk identified:**
- 2 agents (NorthStar, Prime Realty) account for $11K + $53K = **$64K of outstanding**
- Dashboard surfaces this in < 5 seconds

**Scalability:**
- Current: 12 referrals (demo data)
- Production-ready for: 1000s of referrals (just swap CSV for database)

---

## 🚀 Path to Production

**Phase 1 (MVP - Current):** ✅
- Streamlit dashboard with email generator
- Manual copy/paste or Gmail drafts

**Phase 2 (Recommended):**
- Replace CSV with live database (Postgres/Snowflake)
- Move to Retool for better UI controls
- Add Slack notifications for high-priority risks

**Phase 3 (Full Automation):**
- Zapier workflows: "30 days overdue → auto-draft email → Slack alert"
- LLM-powered template selection (GPT-4 analyzes relationship history)
- Bi-directional sync with CRM (Salesforce/HubSpot)

---

## 💡 Why This Matters for HomeLight

**Aligns with role requirements:**
- ✅ "Own referral-to-revenue workflow" → Built the system
- ✅ "AI-first workflows" → Template automation, ready for LLM upgrade  
- ✅ "Own scorecards" → Built KPI dashboard from scratch
- ✅ "Enhance collections" → Agent risk summary + email automation
- ✅ "Cross-functional ready" → Finance can use for reconciliation, Ops for SLAs

**Demonstrates my approach:**
1. **Business first**: Understood the pain point before writing code
2. **Iterate fast**: Built this in 2-3 days, production-ready MVP
3. **Think big, start small**: Designed for scale but shipped quick wins first
4. **Technical + Product**: Can code AND explain why it matters

---

## 🎥 2-Minute Demo Script

1. **Show KPIs** (10s): "Here's our referral pipeline at a glance"
2. **Agent Risk Summary** (20s): "NorthStar Group has $53K outstanding across 2 deals - high priority"
3. **Email Generator** (30s): Select account → Show auto-filled email → "160 days overdue, so it picked the escalation template"
4. **Create Gmail Draft** (20s): Enter email → Click button → "Check Gmail drafts - ready to review and send"
5. **Client Database** (20s): Search "Prime" → Show profile → "Here's the recommended next action"
6. **Wrap** (20s): "This is an MVP built in days. In production, we'd connect to your real data and add Zapier workflows"

---

## 🏆 What I Learned

1. **RevOps requires both precision and speed** - Data must be perfect, but decisions need to be instant
2. **The best tool is the one that gets adopted** - Gmail integration > building a custom email sender
3. **Risk aggregation > risk alerting** - "Which agent" is more actionable than "which deal"
4. **Product sense matters as much as code** - The "repeat offender detection" idea came from thinking about the user's workflow

---

**Built by:** [Your Name]  
**Time to build:** 2-3 days  
**For:** HomeLight Interview Assignment  
**Date:** November 2025

