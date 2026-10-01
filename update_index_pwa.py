import os
import re

print("Reading index.html...")
with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

# 1. iOS & PWA meta tags
ios_meta = """  <meta name="apple-mobile-web-app-capable" content="yes" />
  <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent" />
  <meta name="apple-mobile-web-app-title" content="DBYC Portal" />
  <meta name="mobile-web-app-capable" content="yes" />
  <meta name="application-name" content="DBYC Portal" />
  <meta name="format-detection" content="telephone=no" />
"""
if "apple-mobile-web-app-capable" not in html:
    html = html.replace('<meta name="theme-color" content="#0B5394" />', '<meta name="theme-color" content="#0B5394" />\n' + ios_meta)

# 2. Network Banner after <body>
if 'id="pwaNetworkBanner"' not in html:
    network_banner = """  <!-- PWA NETWORK STATUS BANNER -->
  <div id="pwaNetworkBanner" class="pwa-network-banner">
    <i class="fa-solid fa-wifi" id="pwaNetworkIcon"></i>
    <span id="pwaNetworkText">Online Mode</span>
  </div>
"""
    html = html.replace('<body class="app-body">', '<body class="app-body">\n' + network_banner)

# 3. Sound Toggle & Install Button in top-quick-actions
top_buttons = """        <!-- Sound FX Toggle Button -->
        <button class="btn-top-action btn-sound-toggle" onclick="toggleSoundFx()" id="btnSoundToggle" title="Toggle Sound (ஒலி அமைப்புகள்)">
          <i class="fa-solid fa-volume-high" id="iconSoundToggle"></i>
        </button>

        <!-- PWA Install Button -->
        <button class="btn-top-action btn-pwa-install" onclick="triggerPwaInstall()" id="btnTopInstallPwa" title="Install App (செயலியை நிறுவு)">
          <i class="fa-solid fa-cloud-arrow-down"></i>
        </button>
"""
if 'id="btnSoundToggle"' not in html:
    html = html.replace('<!-- Quick Pass Button -->', top_buttons + '\n        <!-- Quick Pass Button -->')

# 4. Drawer install button
if 'id="btnDrawerInstallPwa"' not in html:
    drawer_install_btn = """      <!-- PWA Install Action in Drawer -->
      <div style="padding: 12px 16px; border-bottom: 1px solid rgba(255,255,255,0.08);">
        <button class="btn btn-warning w-100 btn-pwa-install" onclick="triggerPwaInstall()" id="btnDrawerInstallPwa" style="font-size:13px; padding:10px; font-weight:700;">
          <i class="fa-solid fa-download me-2"></i> <span data-i18n="install_app_button">Install DBYC App (செயலி)</span>
        </button>
      </div>
"""
    html = html.replace('<div class="drawer-menu-scroll">', '<div class="drawer-menu-scroll">\n' + drawer_install_btn)

# 5. Share button in tournament header
if 'shareLiveTournamentScores' not in html:
    html = html.replace(
        '<button class="btn btn-sm btn-outline-danger" onclick="resetTournamentScores()">',
        '<button class="btn btn-sm btn-native-share me-2" onclick="shareLiveTournamentScores()"><i class="fa-brands fa-whatsapp"></i> <span data-i18n="share_scores">Share Scores</span></button>\n        <button class="btn btn-sm btn-outline-danger" onclick="resetTournamentScores()">'
    )

# 6. Share button in Certificate controls
if 'shareCertificateDirect' not in html:
    html = html.replace(
        '<button class="btn btn-outline-secondary" onclick="printCertificate()">',
        '<button class="btn btn-native-share" onclick="shareCertificateDirect()"><i class="fa-brands fa-whatsapp"></i> <span data-i18n="share_cert">Share Certificate</span></button>\n          <button class="btn btn-outline-secondary" onclick="printCertificate()">'
    )

# 7. Share button in ID Card controls
if 'shareIdCardDirect' not in html:
    html = html.replace(
        '<button class="btn btn-outline-secondary" onclick="printIDCard()">',
        '<button class="btn btn-native-share" onclick="shareIdCardDirect()"><i class="fa-brands fa-whatsapp"></i> <span data-i18n="share_id">Share Pass</span></button>\n          <button class="btn btn-outline-secondary" onclick="printIDCard()">'
    )

# 8. iOS Install Guide Modal before </body>
ios_modal = """
  <!-- iOS ADD TO HOME SCREEN INSTRUCTIONS MODAL -->
  <div class="ios-guide-backdrop" id="iosGuideBackdrop" onclick="closeIosInstallGuide()"></div>
  <div class="ios-guide-modal" id="iosGuideModal">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <div class="d-flex align-items-center gap-2">
        <img src="assets/dbyc_official_logo.jpg" style="width:36px; height:36px; border-radius:50%;" alt="DBYC" onerror="this.src='https://via.placeholder.com/36?text=DBYC'">
        <div>
          <h5 class="m-0 font-weight-bold" style="color:var(--navy-primary); font-size:15px;">Install DBYC App</h5>
          <small class="text-muted">iPhone / iPad Safari Installation</small>
        </div>
      </div>
      <button class="btn btn-sm btn-light" onclick="closeIosInstallGuide()"><i class="fa-solid fa-xmark"></i></button>
    </div>
    
    <div class="ios-step">
      <div class="ios-step-badge">1</div>
      <div style="font-size:13px;">
        Tap the <strong>Share</strong> button <i class="fa-solid fa-arrow-up-from-bracket text-primary"></i> at the bottom of your Safari browser.
      </div>
    </div>
    <div class="ios-step">
      <div class="ios-step-badge">2</div>
      <div style="font-size:13px;">
        Scroll down and select <strong>"Add to Home Screen"</strong> <i class="fa-regular fa-square-plus text-primary"></i>.
      </div>
    </div>
    <div class="ios-step">
      <div class="ios-step-badge">3</div>
      <div style="font-size:13px;">
        Tap <strong>"Add"</strong> in the top right corner. The DBYC App will be pinned right to your Home Screen!
      </div>
    </div>
    
    <button class="btn btn-primary w-100 mt-2 font-weight-bold" onclick="closeIosInstallGuide()">
      Got It (புரிந்தது)
    </button>
  </div>
"""

if 'id="iosGuideModal"' not in html:
    html = html.replace('</body>', ios_modal + '\n</body>')

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("index.html written successfully!")
