# Don Bosco Youth Centre (DBYC) - Master Portal & PWA
**Basin Bridge, Chennai - 600 012**

Official Progressive Web Application (PWA), Attendance Scanner, Member Directory, Sports Tournament Center, and Digital ID Pass System.

---

## 🚀 Quick Deployment Guide

You can deploy the DBYC Portal using any of the 4 methods below:

### Option 1: GitHub Pages (100% Free, Automated HTTPS)
1. Create a new GitHub repository (e.g. `dbyc-portal`).
2. Upload the root files (`index.html`, `manifest.json`, `sw.js`, `.nojekyll`, `404.html`, `assets/`, `vercel.json`, `netlify.toml`).
3. In your GitHub repository:
   - Go to **Settings** > **Pages**.
   - Under **Build and deployment** > **Source**, choose **Deploy from a branch**.
   - Select **main** (or **master**) branch and folder `/ (root)`.
   - Click **Save**.
4. Within 1 minute, your live portal URL will be active at:
   `https://<your-username>.github.io/<repo-name>/`

---

### Option 2: Vercel (Fastest Global CDN & Instant Preview)
1. Push your code to GitHub, GitLab, or Bitbucket.
2. Sign in to [Vercel](https://vercel.com) and click **Add New** > **Project**.
3. Import your repository.
4. The included `vercel.json` automatically configures PWA headers, cache rules, and single-page application rewrites.
5. Click **Deploy**. Your custom Vercel domain will be live immediately with automated SSL.

---

### Option 3: Netlify (Drag & Drop or Git CI/CD)
#### Method A: Instant Drag & Drop
1. Sign in to [Netlify](https://app.netlify.com).
2. Go to **Sites** and drag & drop this entire project folder into the Netlify deploy dropzone.
3. Your site is live in under 10 seconds!

#### Method B: Git Repository
1. Connect your repository to Netlify.
2. Build settings are auto-detected via the included `netlify.toml` (publish directory: `.`).
3. Click **Deploy Site**.

---

### Option 4: Google Apps Script (100% Google Cloud, Database & Web App All-in-One)
With this setup, the DBYC portal runs directly on Google's infrastructure with **zero external web hosts**:
1. Go to [script.google.com](https://script.google.com/home/start) and click **+ New project**.
2. Rename the project to `DBYC Master Portal`.
3. In the left files sidebar:
   - Paste the code from `gas/Code.gs` into `Code.gs`.
   - Click **+** > **HTML** and name it `index`.
   - Paste the full content of `gas/index.html` into `index.html`.
4. Click **Deploy** (top right blue button) > **New deployment**.
5. Select **Web app** (gear icon) and set:
   - **Execute as**: `Me (your email)`
   - **Who has access**: `Anyone`
6. Click **Deploy** and grant Google account permissions.
7. Visiting the Web App URL (`https://script.google.com/macros/s/.../exec`) will directly launch the full DBYC portal!
8. When the frontend connects to the backend, it auto-creates the `DBYC_BasinBridge_Database` spreadsheet and `DBYC_Media_Uploads` drive folder.

---

## 📱 PWA Installation
- **Android / Windows / Mac**: Click the **Install DBYC App** button on the top bar or drawer menu, or click the install icon (⊕) in the browser address bar.
- **iPhone / iPad (iOS Safari)**: Tap the **Share** button <i class="fa-solid fa-arrow-up-from-bracket"></i> and select **Add to Home Screen**.

---

## 📁 Repository Structure
```
├── index.html                   # Master single-page application & PWA
├── manifest.json                # Web App Manifest (PWA metadata & icons)
├── sw.js                        # Service Worker (offline app shell cache)
├── .nojekyll                    # Disables Jekyll processing for GitHub Pages
├── 404.html                     # SPA redirect fallback
├── vercel.json                  # Vercel deployment configuration
├── netlify.toml                 # Netlify deployment configuration
├── Code.gs                      # Google Apps Script backend script
├── DBYC_Google_Apps_Script_Code.gs
├── README_GOOGLE_SHEETS_SETUP.md # Google Sheets & Drive sync guide
├── README.md                    # Deployment guide
├── gas/
│   ├── Code.gs                  # GAS backend (serves API & Web App UI)
│   ├── index.html               # GAS standalone HTML file
│   └── appsscript.json          # GAS manifest
└── assets/                      # Icons, official logo, seals, signatures
```
