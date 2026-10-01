with open('index.html', 'r', encoding='utf-8') as f:
    c = f.read()

# 1. Add Minutes drawer link after ID Cards
c = c.replace(
    'ID Cards</span> ID Cards</button>\n    <div class="drawer-section-label">YOUTH LIFE',
    'ID Cards</span> ID Cards</button>\n    <button class="drawer-item" onclick="goPage(\'minutes\');toggleDrawer(false)"><span class="drawer-item-icon">📝</span> DBYC Minutes</button>\n    <div class="drawer-section-label">YOUTH LIFE'
)

# 2. Add Notifications before Rules link
c = c.replace(
    '<span class="drawer-item-icon">📜</span> Rules',
    '<span class="drawer-item-icon">🔔</span> Notifications</button>\n    <button class="drawer-item" onclick="goPage(\'rules\');toggleDrawer(false)"><span class="drawer-item-icon">📜</span> Rules'
)

# 3. Fix – remove the duplicate Rules button added above (prevent double)
# Actually we changed the icon above so let's check. The replacement adds a new button before existing Rules button
# The existing: <button ...><span>📜</span> Rules
# becomes: <span>🔔</span>Notifications</button><button..><span>📜</span> Rules
# But we need to keep the onclick for the Notifications button
c = c.replace(
    'onclick="goPage(\'notifications\');toggleDrawer(false)"><span class="drawer-item-icon">🔔</span> Notifications</button>\n    <button class="drawer-item" onclick="goPage(\'rules\');toggleDrawer(false)"><span class="drawer-item-icon">📜</span> Rules',
    'onclick="goPage(\'notifications\');toggleDrawer(false)"><span class="drawer-item-icon">🔔</span> Notifications</button>\n    <button class="drawer-item" onclick="goPage(\'rules\');toggleDrawer(false)"><span class="drawer-item-icon">📜</span> Rules'
)

# 4. Find the wrong addition and fix — add onclick to notifications button
old_bad = '    <button class="drawer-item" onclick="goPage(\'rules\');toggleDrawer(false)"><span class="drawer-item-icon">🔔</span> Notifications</button>'
new_notif = '    <button class="drawer-item" onclick="goPage(\'notifications\');toggleDrawer(false)"><span class="drawer-item-icon">🔔</span> Notifications</button>'
c = c.replace(old_bad, new_notif)

# 5. Add modals before existing modals comment
minutes_modal = '''<!-- DBYC Minutes Modal -->
<div class="modal-overlay" id="minutesModal">
  <div class="modal-sheet">
    <div class="modal-drag"></div>
    <div class="modal-title-row">
      <span class="modal-title">📝 Add Meeting Minutes</span>
      <button class="modal-close" onclick="closeModal('minutesModal')">✕</button>
    </div>
    <div class="form-field"><label class="auth-label">Meeting Title *</label><input type="text" id="minTitle" class="auth-input" placeholder="e.g. Monthly Meeting"></div>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:8px">
      <div class="form-field"><label class="auth-label">Date *</label><input type="date" id="minDate" class="auth-input"></div>
      <div class="form-field"><label class="auth-label">Group</label>
        <select id="minGroup" class="auth-input">
          <option value="All">All Groups</option>
          <option value="Sub-Junior">Sub-Junior</option>
          <option value="Junior">Junior</option>
          <option value="Inter">Inter</option>
          <option value="Super-Senior">Super-Senior</option>
          <option value="Elder">Elder</option>
        </select>
      </div>
    </div>
    <div class="form-field"><label class="auth-label">Members Present</label><input type="number" id="minAttendees" class="auth-input" placeholder="0" min="0"></div>
    <div class="form-field"><label class="auth-label">Agenda Items</label><textarea id="minAgenda" class="auth-input" style="min-height:80px;resize:vertical" placeholder="1. Opening prayer&#10;2. Last meeting review&#10;3. New business..."></textarea></div>
    <div class="form-field"><label class="auth-label">Decisions / Resolutions</label><textarea id="minDecisions" class="auth-input" style="min-height:80px;resize:vertical" placeholder="Decisions made..."></textarea></div>
    <div class="form-field"><label class="auth-label">Additional Notes</label><textarea id="minNotes" class="auth-input" style="min-height:55px;resize:vertical" placeholder="Other notes..."></textarea></div>
    <button class="auth-btn" onclick="saveMinutes()">Save Minutes</button>
    <div style="height:10px"></div>
  </div>
</div>

<!-- DBYC News Modal -->
<div class="modal-overlay" id="newsModal">
  <div class="modal-sheet">
    <div class="modal-drag"></div>
    <div class="modal-title-row">
      <span class="modal-title" id="newsModalTitle">Post News</span>
      <button class="modal-close" onclick="closeModal('newsModal')">✕</button>
    </div>
    <div class="form-field"><label class="auth-label">Title *</label><input type="text" id="newsTitle" class="auth-input" placeholder="News headline..."></div>
    <div class="form-field"><label class="auth-label">Content *</label><textarea id="newsContent" class="auth-input" style="min-height:100px;resize:vertical" placeholder="Full news content..."></textarea></div>
    <div class="form-field"><label class="auth-label">Category</label>
      <select id="newsCategory" class="auth-input">
        <option value="General">General</option>
        <option value="Event">Event</option>
        <option value="Announcement">Announcement</option>
        <option value="Sports">Sports</option>
        <option value="Prayer">Prayer</option>
        <option value="Achievement">Achievement</option>
        <option value="Alert">Alert</option>
      </select>
    </div>
    <label style="display:flex;align-items:center;gap:8px;font-size:0.85rem;color:#1a237e;cursor:pointer;margin-bottom:14px">
      <input type="checkbox" id="newsPinned" style="width:18px;height:18px;accent-color:#1a237e"> Pin to top
    </label>
    <button class="auth-btn" onclick="saveNews()">Publish News</button>
    <div style="height:10px"></div>
  </div>
</div>

'''

c = c.replace('<!-- ╔══════════ MODALS ══════════╗ -->', minutes_modal + '<!-- ╔══════════ MODALS ══════════╗ -->', 1)

# 6. Add stat-box CSS if missing
stat_css = '''
.stat-box{background:#fff;border-radius:12px;padding:10px 6px;text-align:center;box-shadow:0 2px 8px rgba(0,0,0,0.06);}
.stat-val{font-size:1.4rem;font-weight:900;line-height:1}
.stat-lbl{font-size:0.62rem;color:var(--dbyc-muted,#607d8b);margin-top:3px;font-weight:600}
.filter-chip{background:#e8eaf6;color:#3949ab;border:none;border-radius:20px;padding:6px 12px;font-size:0.75rem;font-weight:700;cursor:pointer;white-space:nowrap;flex-shrink:0}
.filter-chip.filter-active,.filter-chip:active{background:#1a237e;color:#fff}
.tile-deep-orange{background:linear-gradient(135deg,#e65100,#ff8f00)!important}
.btn-sm{font-size:0.75rem;padding:6px 12px;border-radius:10px;border:none;cursor:pointer;font-weight:700}
.btn-blue-sm{background:#1a237e;color:#fff}
.btn-gold-sm{background:var(--dbyc-gold,#ffd700);color:#1a237e}
'''

# Add before </style>
c = c.replace('</style>', stat_css + '\n</style>', 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(c)

print('Patch applied successfully!')
print('Checking Minutes drawer:', 'DBYC Minutes' in c)
print('Checking minutesModal:', 'minutesModal' in c)
print('Checking newsModal:', 'newsModal' in c)
print('Checking stat-box:', 'stat-box' in c)
