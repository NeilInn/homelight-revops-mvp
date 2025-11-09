# Gmail Draft Feature - Quick Start

## ✅ What's Been Implemented

I've added the Gmail Draft feature to your dashboard! Here's what's ready:

### New Features:
1. **📨 "Create Gmail Draft" button** in Email Generator section
2. **Gmail API helper** (`scripts/gmail_helper.py`) for authentication
3. **Setup script** (`scripts/setup_gmail.py`) for easy configuration
4. **Complete setup guide** (`docs/gmail_setup_guide.md`)
5. **Updated requirements.txt** with Google API packages

---

## 🚀 How to Enable It (10 minutes)

### Step 1: Install New Packages

```bash
cd homelight-revops-mvp
pip install -r requirements.txt
```

This installs:
- `google-auth`
- `google-auth-oauthlib`
- `google-auth-httplib2`
- `google-api-python-client`

### Step 2: Get Gmail API Credentials

**Quick version:**
1. Go to [console.cloud.google.com](https://console.cloud.google.com/)
2. Create a new project
3. Enable "Gmail API"
4. Create OAuth 2.0 credentials (Desktop app)
5. Download as `credentials.json`
6. Put it in: `homelight-revops-mvp/credentials.json`

**Detailed version:** See `docs/gmail_setup_guide.md`

### Step 3: Authenticate

```bash
cd homelight-revops-mvp
python scripts/setup_gmail.py
```

This will:
- Check your setup
- Open a browser for Google sign-in
- Ask you to authorize the app
- Save your authentication token

### Step 4: Restart Dashboard

```bash
streamlit run app/streamlit_app.py
```

---

## 🎯 How to Use It

1. **Open dashboard:** http://localhost:8501
2. **Scroll to "📧 Email Generator"**
3. **Select an at-risk account** from dropdown
4. **See the auto-generated email** (subject + body filled in)
5. **Enter the agent's email address**
6. **Click "📨 Create Gmail Draft"**
7. **Check your Gmail** → You'll see a new draft ready to review & send!

---

## 📂 Files Added/Modified

### New Files:
```
homelight-revops-mvp/
├── scripts/
│   ├── gmail_helper.py          # Gmail API integration
│   ├── setup_gmail.py           # Setup wizard
│   └── email_generator.py       # Standalone email generator
├── docs/
│   ├── gmail_setup_guide.md     # Detailed setup instructions
│   └── email_deployment_options.md  # All deployment options
├── .gitignore                   # Protects credentials
└── GMAIL_QUICKSTART.md          # This file
```

### Modified Files:
```
├── app/streamlit_app.py         # Added "Create Gmail Draft" button
├── requirements.txt             # Added Google API packages
└── README.md                    # Updated features list
```

---

## 🔒 Security

**Protected by `.gitignore`:**
- `credentials.json` - Your app credentials (safe, but keep private)
- `token.json` - Your access token (DO NOT SHARE)

These files will NOT be committed to git.

---

## 🧪 Testing Without Setup

The dashboard will run fine without Gmail setup:
- ✅ Email Generator works (copy/paste mode)
- ✅ All other features work normally
- ⚠️ "Create Gmail Draft" button shows as disabled

You can enable it anytime by following the setup steps above.

---

## 🎯 What Happens When You Click the Button

```
User clicks "Create Gmail Draft"
    ↓
App checks for credentials.json
    ↓
App authenticates with Gmail (uses token.json)
    ↓
App creates draft via Gmail API
    ↓
Draft appears in your Gmail drafts folder
    ↓
You review and send!
```

---

## ❓ Need Help?

- **Full setup guide:** `docs/gmail_setup_guide.md`
- **Troubleshooting:** See troubleshooting section in setup guide
- **Alternative options:** `docs/email_deployment_options.md`

---

## 🎉 You're All Set!

Refresh **http://localhost:8501** and try it out!

The Gmail Draft feature makes your workflow:
1. **Faster** - No more copy/pasting
2. **Safer** - Review before sending
3. **Professional** - Emails tracked in your Gmail
4. **Auditable** - Full history in Gmail

Happy collecting! 💰

