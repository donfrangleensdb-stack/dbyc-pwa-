# Let's inspect app.js and append/insert all missing helper and UI functions

ui_functions = '''
// ==========================================
// CORE NAVIGATION, DRAWER & MODAL HELPERS
// ==========================================

function switchView(viewId) {
  const views = [
    'view-home', 'view-form-print', 'view-rules', 'view-birthdays', 
    'view-calendar', 'view-teams', 'view-minutes', 'view-news', 
    'view-scanner', 'view-members', 'view-idcards', 'view-certificates', 
    'view-hierarchy', 'view-points', 'view-settings'
  ];
  
  views.forEach(id => {
    const el = document.getElementById(id);
    if (el) el.style.display = 'none';
  });
  
  const target = document.getElementById(viewId);
  if (target) {
    target.style.display = 'block';
  }
  
  const navMap = {
    'view-home': 'navBtnHome',
    'view-members': 'navBtnMembers',
    'view-scanner': 'navBtnScanner',
    'view-birthdays': 'navBtnBirthdays',
    'view-teams': 'navBtnTeams'
  };
  
  document.querySelectorAll('.nav-item').forEach(btn => btn.classList.remove('active'));
  const activeNavId = navMap[viewId];
  if (activeNavId) {
    const navBtn = document.getElementById(activeNavId);
    if (navBtn) navBtn.classList.add('active');
  }
  
  toggleNavigationDrawer(false);
  window.scrollTo({ top: 0, behavior: 'smooth' });
  
  if (viewId === 'view-home') {
    renderLeaderboard();
    renderTeamsScoreboard();
  } else if (viewId === 'view-members') {
    renderMembersRegistry();
  } else if (viewId === 'view-teams') {
    renderTeamsScoreboard();
    renderCurrentTeamMembersList();
  } else if (viewId === 'view-rules') {
    render15Rules();
  } else if (viewId === 'view-birthdays') {
    renderBirthdays();
  } else if (viewId === 'view-calendar') {
    renderEvents();
  } else if (viewId === 'view-minutes') {
    renderMinutes();
  } else if (viewId === 'view-news') {
    renderNews();
  } else if (viewId === 'view-idcards') {
    generateIDCardPreview();
  } else if (viewId === 'view-certificates') {
    generateCertificatePreview();
  }
}

function toggleNavigationDrawer(open) {
  const drawer = document.getElementById('sideDrawer');
  const backdrop = document.getElementById('drawerBackdrop');
  if (open) {
    if (drawer) drawer.classList.add('open');
    if (backdrop) backdrop.classList.add('open');
  } else {
    if (drawer) drawer.classList.remove('open');
    if (backdrop) backdrop.classList.remove('open');
  }
}

function navigateFromDrawer(viewId) {
  switchView(viewId);
  toggleNavigationDrawer(false);
}

function showToast(message, type = 'info') {
  let toastContainer = document.getElementById('appToastContainer');
  if (!toastContainer) {
    toastContainer = document.createElement('div');
    toastContainer.id = 'appToastContainer';
    toastContainer.className = 'app-toast-container';
    document.body.appendChild(toastContainer);
  }
  const toast = document.createElement('div');
  toast.className = `app-toast toast-${type}`;
  const iconClass = type === 'error' ? 'triangle-exclamation' : type === 'success' ? 'check-circle' : 'circle-info';
  toast.innerHTML = `<i class="fa-solid fa-${iconClass}"></i> <span>${message}</span>`;
  toastContainer.appendChild(toast);
  setTimeout(() => { toast.classList.add('show'); }, 10);
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => { toast.remove(); }, 400);
  }, 3500);
}

function closeModal(modalId) {
  const el = document.getElementById(modalId);
  if (el) {
    el.style.display = 'none';
    el.classList.remove('show', 'open', 'active');
  }
}

function openModal(modalId) {
  const el = document.getElementById(modalId);
  if (el) {
    el.style.display = 'flex';
    el.classList.add('show', 'open', 'active');
  }
}

function showLoginModal() { openModal('loginModal'); }
function hideLoginModal() { closeModal('loginModal'); }
function closeLoginModal() { closeModal('loginModal'); }

function openAwardPointsModal(memberId) {
  const select = document.getElementById('awardPointsMemberSelect');
  if (select && memberId) select.value = memberId;
  openModal('awardPointsModal');
}

function closeAwardPointsModal() { closeModal('awardPointsModal'); }

function openAIAssistantModal() { openModal('aiAssistantModal'); }
function closeAIAssistantModal() { closeModal('aiAssistantModal'); }

function sendAIMessage() {
  const input = document.getElementById('aiMessageInput');
  const chatBody = document.getElementById('aiChatBody');
  if (!input || !chatBody) return;
  const msg = input.value.trim();
  if (!msg) return;
  
  const userBubble = document.createElement('div');
  userBubble.className = 'ai-bubble ai-bubble-user';
  userBubble.textContent = msg;
  chatBody.appendChild(userBubble);
  input.value = '';
  
  const botBubble = document.createElement('div');
  botBubble.className = 'ai-bubble ai-bubble-bot';
  botBubble.textContent = 'Thinking... 🙏';
  chatBody.appendChild(botBubble);
  chatBody.scrollTop = chatBody.scrollHeight;
  
  setTimeout(() => {
    let reply = "May the grace of St. John Bosco guide you. Keep active in attendance and earn points for your team!";
    const lower = msg.toLowerCase();
    if (lower.includes('rule') || lower.includes('age') || lower.includes('group')) {
      reply = "DBYC groups: Sub-Junior (6-14), Junior (15-18), Inter (19-24), Super-Senior (25-35), Elder (35+). 75% attendance is required per Rule 3.";
    } else if (lower.includes('point') || lower.includes('score')) {
      reply = "Points: Present = +10, Late = +5, Tournament Goal = +20, Perfect Month = +50!";
    } else if (lower.includes('prayer') || lower.includes('bless')) {
      reply = "'Give me souls, take away the rest.' – St. John Bosco. God bless your youth and dedication!";
    }
    botBubble.textContent = reply;
    chatBody.scrollTop = chatBody.scrollHeight;
  }, 600);
}

function askAISuggestion(promptText) {
  const input = document.getElementById('aiMessageInput');
  if (input) {
    input.value = promptText;
    sendAIMessage();
  }
}

function filterMembersByGroup(group) {
  document.querySelectorAll('.filter-pill-btn').forEach(b => b.classList.remove('active'));
  const btn = event?.target;
  if (btn) btn.classList.add('active');
  renderMembersRegistry(group);
}

let currentCalYear = 2024;
let currentCalMonth = 8; // September

function navigateCalendarMonth(delta) {
  currentCalMonth += delta;
  if (currentCalMonth > 11) { currentCalMonth = 0; currentCalYear++; }
  if (currentCalMonth < 0) { currentCalMonth = 11; currentCalYear--; }
  renderEvents();
}

function launchBirthdayConfetti() {
  showToast('🎉 Happy Birthday to all DBYC Celebrants! 🎂 God Bless!', 'success');
}

function setScannerMode(mode) {
  const camSec = document.getElementById('cameraScannerSection');
  const manSec = document.getElementById('manualScannerSection');
  const camBtn = document.getElementById('btnModeCamera');
  const manBtn = document.getElementById('btnModeManual');
  
  if (mode === 'camera') {
    if (camSec) camSec.style.display = 'block';
    if (manSec) manSec.style.display = 'none';
    if (camBtn) camBtn.classList.add('active');
    if (manBtn) manBtn.classList.remove('active');
    startQRScanner();
  } else {
    if (camSec) camSec.style.display = 'none';
    if (manSec) manSec.style.display = 'block';
    if (camBtn) camBtn.classList.remove('active');
    if (manBtn) manBtn.classList.add('active');
    stopQRScanner();
  }
}

function startQRScanner() {
  startCameraScanner();
}

function stopQRScanner() {
  const video = document.getElementById('scannerVideo');
  if (video && video.srcObject) {
    video.srcObject.getTracks().forEach(t => t.stop());
    video.srcObject = null;
  }
}

function dismissScanResult() {
  closeModal('scanResultModal');
}

function openCertificateForCurrentScan() {
  closeModal('scanResultModal');
  const id = document.getElementById('scanResultId')?.textContent;
  if (id) jumpToCertificate(id);
}

function exportMembersCSV() {
  let csv = 'Member ID,Name,Group,Role,Mobile,Age,Points,Attendance Pct\\n';
  appData.members.forEach(m => {
    csv += `"${m.id}","${m.name}","${m.group}","${m.role}","${m.mobile}","${calculateAge(m.dob)}","${m.points}","${calcAttendancePct(m.id)}%"\\n`;
  });
  const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `DBYC_Members_${new Date().toISOString().split('T')[0]}.csv`;
  a.click();
  showToast('Members list exported as CSV!', 'success');
}

function exportDatabaseJSON() {
  const json = JSON.stringify(appData, null, 2);
  const blob = new Blob([json], { type: 'application/json' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `DBYC_Backup_${new Date().toISOString().split('T')[0]}.json`;
  a.click();
  showToast('Database exported as JSON backup!', 'success');
}

function resetDemoData() {
  if (confirm('Reset all DBYC data to initial official defaults?')) {
    localStorage.removeItem(STORAGE_KEY);
    localStorage.removeItem(AUTH_STORAGE_KEY);
    location.reload();
  }
}

let isTamilLang = false;
function toggleLanguage() {
  isTamilLang = !isTamilLang;
  const lbl = document.getElementById('drawerLangLabel');
  if (lbl) lbl.textContent = isTamilLang ? 'தமிழ் (TA)' : 'English (EN)';
  showToast(isTamilLang ? 'மொழி மாற்றப்பட்டது: தமிழ்' : 'Language set to English', 'info');
}

function toggleVoiceAssistant() {
  showToast('Voice Assistant activated: Speak "Mark attendance" or "Show birthdays"', 'info');
}

function selectSalesianTheme(themeKey) {
  document.body.className = `theme-${themeKey}`;
  showToast(`Salesian Theme updated: ${themeKey.toUpperCase()}`, 'success');
}

function updateNewsTicker() {
  const tickerEl = document.getElementById('newsTickerText');
  if (tickerEl && appData.news && appData.news.length > 0) {
    tickerEl.textContent = appData.news.map(n => `📢 [${n.date}] ${n.title}: ${n.content}`).join('   •   ');
  }
}

function clearActivityFeed() {
  appData.activityFeed = [];
  saveAppData();
  showToast('Activity feed cleared', 'info');
}

function quickSwitchUserPhoto(memberId) {
  const m = appData.members.find(x => x.id === memberId);
  if (m) {
    const url = prompt('Enter image URL or Base64 data for profile photo:', m.photo);
    if (url) {
      m.photo = url;
      saveAppData();
      renderMembersRegistry();
      showToast('Photo updated successfully!', 'success');
    }
  }
}
'''

with open('app.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Append UI helper functions to app.js
with open('app.js', 'w', encoding='utf-8') as f:
    f.write(js + '\n\n' + ui_functions)

print('Updated app.js with all UI and navigation functions!')
