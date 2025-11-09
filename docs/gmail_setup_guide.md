# Gmail API Setup Guide - Create Drafts from Dashboard

Follow these steps to enable the "Create Gmail Draft" feature in your dashboard.

## ⏱️ Time Required: 5-10 minutes

---

## Step 1: Install Required Packages

```bash
cd homelight-revops-mvp
pip install -r requirements.txt
```

This installs the Google API libraries.

---

## Step 2: Set Up Google Cloud Project

### 2.1 Create a Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it: `homelight-revops-mvp` (or anything you prefer)
4. Click "Create"

### 2.2 Enable Gmail API

1. In the search bar at top, type: **"Gmail API"**
2. Click on "Gmail API" in results
3. Click the blue **"Enable"** button
4. Wait ~30 seconds for it to activate

---

## Step 3: Create OAuth Credentials

### 3.1 Configure OAuth Consent Screen

1. Go to **"APIs & Services"** → **"OAuth consent screen"**
2. Select **"External"** (unless you have a Google Workspace)
3. Click **"Create"**

Fill in:
- **App name:** `HomeLight RevOps MVP`
- **User support email:** Your email
- **Developer contact:** Your email
- Click **"Save and Continue"**

### 3.2 Add Scopes (Optional)

- Click **"Save and Continue"** (no changes needed)

### 3.3 Add Test Users

- Click **"Add Users"**
- Enter YOUR email address (the Gmail you'll use)
- Click **"Save and Continue"**

### 3.4 Create Credentials

1. Go to **"APIs & Services"** → **"Credentials"**
2. Click **"+ Create Credentials"** → **"OAuth client ID"**
3. Select **"Desktop app"** as application type
4. Name it: `HomeLight Desktop Client`
5. Click **"Create"**

### 3.5 Download Credentials

1. You'll see a popup with your client ID
2. Click **"Download JSON"**
3. Rename the downloaded file to: **`credentials.json`**
4. Move it to your project root: `homelight-revops-mvp/credentials.json`

**Your folder should look like:**
```
homelight-revops-mvp/
├── credentials.json  ← NEW FILE HERE
├── app/
├── data/
├── scripts/
└── requirements.txt
```

---

## Step 4: Test the Connection

Run this command to authenticate for the first time:

```bash
cd homelight-revops-mvp
python scripts/gmail_helper.py
```

**What happens:**
1. A browser window opens
2. Google asks you to sign in
3. Google asks: "HomeLight RevOps MVP wants to manage your drafts"
4. Click **"Allow"**
5. You'll see: ✅ Successfully connected to Gmail: your@email.com

**This creates `token.json`** which stores your authentication for future use.

---

## Step 5: Run Your Dashboard

```bash
streamlit run app/streamlit_app.py
```

You'll now see a **"Create Gmail Draft"** button in the Email Generator section!

---

## 🔒 Security Notes

- ✅ **`credentials.json`** contains your app's ID (safe to keep)
- ⚠️ **`token.json`** contains YOUR access token (don't share or commit to git)
- Add to `.gitignore`:
  ```
  token.json
  credentials.json
  ```

---

## 🐛 Troubleshooting

### "Missing credentials.json"
→ Make sure the file is in the project root, not in a subfolder

### "Access blocked: This app's request is invalid"
→ Make sure you selected "Desktop app" (not "Web app") when creating credentials

### Browser doesn't open for authentication
→ Try: `python scripts/gmail_helper.py` manually first

### "Insufficient Permission"
→ Delete `token.json` and re-run to re-authenticate

---

## ✅ You're Done!

Now when you:
1. Select an account in the Email Generator
2. Click "Create Gmail Draft"
3. A draft appears in your Gmail ready to review and send!

No more copy/pasting! 🎉

