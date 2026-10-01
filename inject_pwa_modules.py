import sys
sys.stdout.reconfigure(encoding='utf-8')

print("Reading app.js...")
with open("app.js", "r", encoding="utf-8") as f:
    app_js = f.read()

pwa_engine_code = '''
// ======================================================
// 0. PROGRESSIVE WEB APP (PWA) ENGINES & NATIVE CAPABILITIES
// ======================================================

const SOUND_MUTED_KEY = 'DBYC_SOUND_MUTED_V1';

/**
 * Web Audio API Sound Synthesizer (0 external mp3 dependencies)
 */
const SoundFx = {
  ctx: null,
  isMuted: false,

  init() {
    this.isMuted = localStorage.getItem(SOUND_MUTED_KEY) === 'true';
    this.updateToggleIcon();
  },

  getContext() {
    if (!this.ctx) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (AudioContextClass) {
        this.ctx = new AudioContextClass();
      }
    }
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume().catch(() => {});
    }
    return this.ctx;
  },

  play(type) {
    if (this.isMuted) return;
    try {
      const ctx = this.getContext();
      if (!ctx) return;
      const now = ctx.currentTime;

      if (type === 'tap' || type === 'click') {
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(440, now);
        osc.frequency.exponentialRampToValueAtTime(220, now + 0.05);
        gain.gain.setValueAtTime(0.12, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.05);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.05);
      } else if (type === 'success') {
        // Dual-tone uplifting chime
        [523.25, 659.25, 783.99].forEach((freq, idx) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'triangle';
          osc.frequency.setValueAtTime(freq, now + idx * 0.08);
          gain.gain.setValueAtTime(0.15, now + idx * 0.08);
          gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.08 + 0.25);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now + idx * 0.08);
          osc.stop(now + idx * 0.08 + 0.25);
        });
      } else if (type === 'scan') {
        // Electronic barcode reader beep
        const osc = ctx.createOscillator();
        const gain = ctx.createGain();
        osc.type = 'sine';
        osc.frequency.setValueAtTime(1760, now);
        gain.gain.setValueAtTime(0.2, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.12);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.12);
      } else if (type === 'score') {
        // Victory Fanfare Chord (C5 - E5 - G5 - C6)
        [523.25, 659.25, 783.99, 1046.50].forEach((freq, idx) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sine';
          osc.frequency.setValueAtTime(freq, now + idx * 0.06);
          gain.gain.setValueAtTime(0.18, now + idx * 0.06);
          gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.06 + 0.3);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now + idx * 0.06);
          osc.stop(now + idx * 0.06 + 0.3);
        });
      } else if (type === 'error') {
        // Low error buzz
        [220, 180].forEach((freq, idx) => {
          const osc = ctx.createOscillator();
          const gain = ctx.createGain();
          osc.type = 'sawtooth';
          osc.frequency.setValueAtTime(freq, now + idx * 0.08);
          gain.gain.setValueAtTime(0.15, now + idx * 0.08);
          gain.gain.exponentialRampToValueAtTime(0.001, now + idx * 0.08 + 0.15);
          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now + idx * 0.08);
          osc.stop(now + idx * 0.08 + 0.15);
        });
      }
    } catch (e) {
      console.warn('Audio synthesis note:', e);
    }
  },

  toggle() {
    this.isMuted = !this.isMuted;
    localStorage.setItem(SOUND_MUTED_KEY, this.isMuted ? 'true' : 'false');
    this.updateToggleIcon();
    showToast(this.isMuted ? '🔇 Sound Muted (ஒலி முடக்கப்பட்டது)' : '🔊 Sound Enabled (ஒலி இயக்கப்பட்டது)');
    if (!this.isMuted) this.play('tap');
  },

  updateToggleIcon() {
    const btn = document.getElementById('btnSoundToggle');
    const icon = document.getElementById('iconSoundToggle');
    if (!icon) return;
    if (this.isMuted) {
      icon.className = 'fa-solid fa-volume-xmark';
      btn?.classList.add('muted');
    } else {
      icon.className = 'fa-solid fa-volume-high';
      btn?.classList.remove('muted');
    }
  }
};

/**
 * Haptic Vibration Engine with graceful fallbacks
 */
const Haptics = {
  vibrate(pattern) {
    if ('vibrate' in navigator) {
      try {
        navigator.vibrate(pattern);
      } catch (e) {}
    }
  },
  light() { this.vibrate(20); },
  medium() { this.vibrate(45); },
  success() { this.vibrate([30, 40, 60]); },
  score() { this.vibrate([50, 30, 80]); },
  error() { this.vibrate([80, 50, 80]); }
};

/**
 * PWA Installation Manager (beforeinstallprompt, iOS Safari guide, Standalone detection)
 */
const PwaManager = {
  deferredPrompt: null,
  isIos: /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream,
  isStandalone: window.matchMedia('(display-mode: standalone)').matches || window.navigator.standalone === true,

  init() {
    window.addEventListener('beforeinstallprompt', (e) => {
      e.preventDefault();
      this.deferredPrompt = e;
      this.showInstallButtons(true);
      console.log('[PWA] beforeinstallprompt event captured.');
    });

    window.addEventListener('appinstalled', () => {
      this.deferredPrompt = null;
      this.showInstallButtons(false);
      showToast('🎉 DBYC App installed successfully! (செயலி வெற்றிகரமாக நிறுவப்பட்டது)');
      confetti({ particleCount: 60, spread: 70, origin: { y: 0.6 } });
      SoundFx.play('success');
      Haptics.success();
    });

    if (this.isStandalone) {
      console.log('[PWA] Running in Standalone Display Mode');
      this.showInstallButtons(false);
    }
  },

  showInstallButtons(visible) {
    const topBtn = document.getElementById('btnTopInstallPwa');
    const drawerBtn = document.getElementById('btnDrawerInstallPwa');
    if (topBtn) topBtn.style.display = visible ? 'inline-flex' : 'none';
    if (drawerBtn) drawerBtn.style.display = visible ? 'block' : 'none';
  },

  async install() {
    Haptics.light();
    SoundFx.play('tap');

    if (this.deferredPrompt) {
      this.deferredPrompt.prompt();
      const { outcome } = await this.deferredPrompt.userChoice;
      console.log(`[PWA] Install prompt outcome: ${outcome}`);
      if (outcome === 'accepted') {
        this.deferredPrompt = null;
        this.showInstallButtons(false);
      }
    } else if (this.isIos) {
      openIosInstallGuide();
    } else {
      // If already installed or browser doesn't trigger prompt
      showToast('💡 Use your browser menu -> "Install App" or "Add to Home Screen"');
      openIosInstallGuide();
    }
  }
};

/**
 * Native Web Share API (WhatsApp / Telegram / System Sheet integration)
 */
const NativeShare = {
  async share(data) {
    Haptics.light();
    SoundFx.play('tap');

    if (navigator.share) {
      try {
        await navigator.share(data);
        showToast('✅ Shared successfully! (பகிரப்பட்டது)');
        return true;
      } catch (err) {
        if (err.name !== 'AbortError') {
          console.warn('Web Share failed, falling back:', err);
        }
      }
    }
    
    // Fallback: WhatsApp Direct URL
    const textToShare = encodeURIComponent(`${data.title}\\n\\n${data.text || ''}\\n${data.url || window.location.href}`);
    const whatsappUrl = `https://api.whatsapp.com/send?text=${textToShare}`;
    window.open(whatsappUrl, '_blank');
    return false;
  }
};

/**
 * Live Network Connectivity Watcher
 */
const NetworkWatcher = {
  init() {
    window.addEventListener('online', () => this.updateStatus(true));
    window.addEventListener('offline', () => this.updateStatus(false));
    if (!navigator.onLine) this.updateStatus(false);
  },

  updateStatus(isOnline) {
    const banner = document.getElementById('pwaNetworkBanner');
    const icon = document.getElementById('pwaNetworkIcon');
    const text = document.getElementById('pwaNetworkText');
    if (!banner || !text || !icon) return;

    if (isOnline) {
      banner.className = 'pwa-network-banner show online';
      icon.className = 'fa-solid fa-wifi';
      text.textContent = currentLanguage === 'ta' ? '🟢 ஆன்லைன் - DBYC தளம் இணைக்கப்பட்டுள்ளது' : '🟢 Online - DBYC Cloud Connected';
      setTimeout(() => { banner.classList.remove('show'); }, 3000);
      SoundFx.play('success');
    } else {
      banner.className = 'pwa-network-banner show offline';
      icon.className = 'fa-solid fa-plane-slash';
      text.textContent = currentLanguage === 'ta' ? '📡 ஆஃப்லைன் பயன்முறை - அனைத்து DBYC அம்சங்களும் கிடைக்கும்' : '📡 Offline Mode - All Local Features Ready';
      SoundFx.play('error');
      Haptics.error();
    }
  }
};

// Global Helper Wrappers for HTML onclick handlers
function toggleSoundFx() { SoundFx.toggle(); }
function triggerPwaInstall() { PwaManager.install(); }
function openIosInstallGuide() {
  document.getElementById('iosGuideBackdrop')?.classList.add('show');
  document.getElementById('iosGuideModal')?.classList.add('show');
}
function closeIosInstallGuide() {
  document.getElementById('iosGuideBackdrop')?.classList.remove('show');
  document.getElementById('iosGuideModal')?.classList.remove('show');
}

function shareLiveTournamentScores() {
  const scores = appData.tournamentScores || { don_bosco: 150, dominic_savio: 120, mamma_margaret: 140, michael_magone: 110 };
  const names = appData.tournamentTeamNames || { don_bosco: 'Don Bosco (Blue)', dominic_savio: 'Dominic Savio (Green)', mamma_margaret: 'Mamma Margaret (Red)', michael_magone: 'Michael Magone (Gold)' };

  const message = `🏆 *DBYC 4-TEAMS TOURNAMENT LIVE STANDINGS* 🏆\\nDon Bosco Youth Centre, Basin Bridge, Chennai - 600 012\\n\\n` +
    `🔵 ${names.don_bosco}: *${scores.don_bosco} Pts*\\n` +
    `🟢 ${names.dominic_savio}: *${scores.dominic_savio} Pts*\\n` +
    `🔴 ${names.mamma_margaret}: *${scores.mamma_margaret} Pts*\\n` +
    `🟡 ${names.michael_magone}: *${scores.michael_magone} Pts*\\n\\n` +
    `🔗 Live Portal: ${window.location.href}`;

  NativeShare.share({
    title: 'DBYC Tournament Live Standings',
    text: message,
    url: window.location.href
  });
}

function shareCertificateDirect() {
  const name = document.getElementById('certNameInput')?.value || 'Honored Member';
  const reason = document.getElementById('certReasonInput')?.value || 'Active Participation & Excellence';
  const message = `📜 *DON BOSCO YOUTH CENTRE - OFFICIAL CERTIFICATE OF EXCELLENCE* 📜\\nBasin Bridge, Chennai - 600 012\\n\\n` +
    `Awarded To: *${name}*\\n` +
    `Reason: *${reason}*\\n` +
    `Signed By: Director & Assistant Director, DBYC\\n\\n` +
    `Verified at: ${window.location.href}`;

  NativeShare.share({
    title: `DBYC Certificate - ${name}`,
    text: message,
    url: window.location.href
  });
}

function shareIdCardDirect() {
  const user = getActiveUser();
  const message = `🪪 *DBYC OFFICIAL DIGITAL PASS* 🪪\\nDon Bosco Youth Centre, Basin Bridge, Chennai - 600 012\\n\\n` +
    `Member: *${user.name}*\\n` +
    `ID No: *${user.id}*\\n` +
    `Designation: *${user.role}*\\n` +
    `Team: *${user.team}*\\n\\n` +
    `Access Portal: ${window.location.href}`;

  NativeShare.share({
    title: `DBYC Digital Pass - ${user.name}`,
    text: message,
    url: window.location.href
  });
}
'''

# Insert the PWA Engine right at the top of app.js after header comments
if "const SOUND_MUTED_KEY =" not in app_js:
    # Insert after initial comments
    comment_end = app_js.find('// ==========================================')
    if comment_end != -1:
        app_js = app_js[:comment_end] + pwa_engine_code + '\n' + app_js[comment_end:]
    else:
        app_js = pwa_engine_code + '\n' + app_js

# Enhance switchView to play sound and trigger haptics
app_js = app_js.replace(
    'function switchView(viewId) {',
    'function switchView(viewId) {\n  SoundFx.play("tap");\n  Haptics.light();'
)

# Enhance modifyTeamScore to play victory fanfare and trigger score haptics
app_js = app_js.replace(
    'function modifyTeamScore(teamKey, delta) {',
    'function modifyTeamScore(teamKey, delta) {\n  if (delta > 0) { SoundFx.play("score"); Haptics.score(); confetti({ particleCount: 35, spread: 50, origin: { y: 0.7 } }); } else { SoundFx.play("error"); Haptics.light(); }'
)

# Enhance check-in / manual attendance
app_js = app_js.replace(
    'function manualAttendanceSubmit() {',
    'function manualAttendanceSubmit() {\n  SoundFx.play("scan");\n  Haptics.success();'
)

# Enhance loginSuccess
app_js = app_js.replace(
    'function loginSuccess(user, role) {',
    'function loginSuccess(user, role) {\n  SoundFx.play("success");\n  Haptics.success();'
)

# Enhance DOMContentLoaded
dom_init_snippet = """  // PWA Initializations
  SoundFx.init();
  PwaManager.init();
  NetworkWatcher.init();

  // Deep Link View Routing (from PWA Shortcuts or Bookmarks)
  try {
    const urlParams = new URLSearchParams(window.location.search);
    const viewParam = urlParams.get('view');
    if (viewParam) {
      const targetView = viewParam.startsWith('view-') ? viewParam : 'view-' + viewParam;
      setTimeout(() => {
        switchView(targetView);
        showToast(`📱 Opened: ${viewParam}`);
      }, 250);
    }
  } catch (err) {
    console.log('Deep link check note:', err);
  }
"""

if "SoundFx.init();" not in app_js:
    app_js = app_js.replace(
        "checkAuthSession();",
        "checkAuthSession();\n" + dom_init_snippet
    )

with open("app.js", "w", encoding="utf-8") as f:
    f.write(app_js)

print("app.js updated successfully with all PWA capabilities!")
