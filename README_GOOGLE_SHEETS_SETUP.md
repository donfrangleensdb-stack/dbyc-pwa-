# DBYC Basin Bridge - Google Sheets & Drive Setup Guide

## 1. Deploying the Google Apps Script Backend (Code.gs)
1. Go to [script.google.com](https://script.google.com/home/start) and sign in with your Google account.
2. Click **+ New project**.
3. Replace all default code with the contents of `DBYC_Google_Apps_Script_Code.gs`.
4. Click **Deploy** (top right blue button) > **New deployment**.
5. Select type: **Web app** (click the gear icon).
6. Configure settings:
   - **Description**: `DBYC Master Backend`
   - **Execute as**: `Me (your email)`
   - **Who has access**: `Anyone`
7. Click **Deploy** and authorize permissions with your Google Account.
8. Copy the **Web App URL** (ends in `/exec`).

## 2. Connecting to DBYC App
1. Open the DBYC Web App.
2. In **Master Settings** (or by clicking the Sync dot on the top navbar), paste your Web App URL into the Google Apps Script Endpoint field.
3. Click **Save URL & Connect**.

## 3. What Happens Automatically:
- A Google Spreadsheet named `DBYC_BasinBridge_Database` is automatically created in your Google Drive with tabs:
  - `Members` (All member registration records)
  - `Attendance` (Daily attendance records)
  - `News` (Announcements & Flash news)
  - `Events` (Calendar events)
  - `Minutes` (Council minutes)
  - `Qualifications` (Approval Desk items)
  - `Matches` (Live sports scores)
- A Google Drive folder named `DBYC_Media_Uploads` is automatically created for all photos and videos.
- All devices automatically refresh every 10 seconds.
- Member registration is 100% friction-free with **NO CAPTCHA**.
