# DBYC - Don Bosco Youth Centre Progressive Web Application (PWA)
### Salesian Province of Chennai (INM Province - Salesians of Don Bosco)

A responsive, zero-budget, multi-platform Progressive Web Application (PWA) designed for **Don Bosco Youth Centre (DBYC)**. Works seamlessly on **Android, iPhone, iPads/Tablets, and Desktop browsers**.

---

## 🌟 Key Architecture & Highlights

* **Frontend**: Pure HTML5, CSS3, JavaScript (zero external bulky build tools; 100% GitHub Pages ready).
* **Backend**: **Google Apps Script (`Code.gs`)** (handles API dispatching, CRUD, QR Attendance logging).
* **Database**: **Google Sheets** (structured with 6 dedicated tabs).
* **Budget**: **\$0.00 / month forever** (uses free GitHub hosting + Google Workspace cloud infrastructure).
* **Role Hierarchy & Organization Structure**:
  * **Rev. Fr. Director** (Incharge)
  * **Rev. Fr. Assistant Director** (Direct Incharge)
  * **Group Leaders & Incharges** for all 6 DBYC Youth Categories:
    1. 🏆 **Sub Juniors Group**
    2. 🏆 **Junior Group**
    3. 🏆 **Senior Group**
    4. 🏆 **Inters Group**
    5. 🏆 **Super Seniors Group**
    6. 🏆 **Elders Group**

---

## 📱 Modules Included

1. **Login Portal**:
   * Custom UI matching the Salesian Province of Chennai theme with Don Bosco silhouette artwork.
   * Phone Number / Member ID authentication with role detection.
2. **Operations Dashboard**:
   * Don Bosco & Mary Help of Christians header crest with INM founding ribbon.
   * Real-time scrolling Province News Marquee ticker.
   * Quick-access colorful glossy 4-column application grid.
   * Real-time metrics for total members, today's attendance count, and active events.
3. **Members Registry**:
   * Filterable by all 6 groups with search by Name, ID, or Mobile.
   * Real-time tenure calculator showing exact years, months, and days in DBYC.
   * Member profile modal with blood group, guardian details, and attendance count.
4. **QR Attendance System**:
   * Built-in live camera QR Scanner for scanning member QR passes.
   * Manual Check-in fallback for instant check-in.
   * Real-time check-in log with timestamps and attendance badges.
5. **Member Digital QR Passes (ID Cards)**:
   * Official DBYC ID Card with DBYC circular logo and Salesian header.
   * Dynamic high-resolution QR verification code with member payload.
   * One-click print or download pass.
6. **Auto Certificate Studio**:
   * **Official Certificate of Membership**: Auto-populated with member's name, DBYC ID, group, tenure, and Salesian leadership signatures.
   * **Certificate of Attendance Excellence**: Awarded based on regularity records.
   * Print-ready and downloadable directly from browser.
7. **Birthday Celebrations**:
   * Current month birthday feed with one-click **WhatsApp Birthday Greeting** direct link.
8. **Event Calendar & Upcoming Events**:
   * Schedule youth tournaments, retreats, meetings, and feast celebrations.
9. **DBYC Minutes of Meeting**:
   * Council meeting records with agendas, attendees, and action items presided by the Director & Assistant Director.
10. **DBYC News & Updates**:
    * Province bulletins and centre announcements.

---

## 🚀 Step-by-Step Deployment Guide

### Step 1: Google Sheets & Google Apps Script Setup
1. Go to [sheets.new](https://sheets.new) to create a new Google Sheet. Name it `DBYC Database`.
2. In the top menu, click **Extensions** > **Apps Script**.
3. Replace the code in `Code.gs` with the code in [`gas/Code.gs`](file:///C:/Users/acer/.gemini/antigravity/scratch/dbyc-pwa/gas/Code.gs).
4. Click **Deploy** (top right) > **New deployment**:
   * Select type: ⚙️ **Web app**.
   * Description: `DBYC API v2`.
   * Execute as: `Me (your email)`.
   * Who has access: `Anyone`.
5. Click **Deploy**, authorize permissions, and **copy the Web App URL** (e.g., `https://script.google.com/macros/s/.../exec`).

---

### Step 2: Connect Frontend to Google Sheets
1. Open [`index.html`](file:///C:/Users/acer/.gemini/antigravity/scratch/dbyc-pwa/index.html) in your browser.
2. In the sidebar menu, open **Google Sheets Sync** (or Settings).
3. Paste your copied Google Apps Script Web App URL and click **Save Endpoint** & **Sync with Google Sheets**.

---

### Step 3: Publish on GitHub & Enable GitHub Pages (Free Hosting)
1. Initialize git in this project folder:
   ```bash
   git init
   git add .
   git commit -m "Initial commit of DBYC PWA"
   ```
2. Create a new repository on [github.com](https://github.com) named `dbyc-pwa`.
3. Push your code:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/dbyc-pwa.git
   git branch -M main
   git push -u origin main
   ```
4. Go to **Settings** > **Pages** in your GitHub repository:
   * Source: `Deploy from a branch`.
   * Branch: `main` / `/(root)`.
   * Click **Save**.
5. Your live app URL will be: `https://YOUR_USERNAME.github.io/dbyc-pwa/`

---

## 📲 Installing as a PWA on Mobile Devices

* **Android (Chrome)**: Open the URL > tap the three dots (⋮) > tap **Install App** or **Add to Home screen**.
* **iPhone / iPad (Safari)**: Open the URL > tap the Share icon (⎙ / ⬆️) > tap **Add to Home Screen**.
* **Desktop (Chrome / Edge)**: Click the **Install** icon in the address bar.
