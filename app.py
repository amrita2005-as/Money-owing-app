import streamlit as st
import sqlite3
from datetime import datetime
import hashlib
import urllib.parse

st.set_page_config(page_title="OweNo", layout="centered", page_icon="💸")

# ── SVG icon library ──────────────────────────────────────────────────────────
def icon(name, size=16, color="currentColor", extra=""):
    paths = {
        # trash / delete
        "trash": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" {extra}><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6"/><path d="M14 11v6"/><path d="M9 6V4a1 1 0 0 1 1-1h4a1 1 0 0 1 1 1v2"/></svg>',
        # whatsapp / send reminder
        "send": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" {extra}><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>',
        # check / confirm
        "check": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" {extra}><polyline points="20 6 9 17 4 12"/></svg>',
        # x / cancel
        "x": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" {extra}><line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/></svg>',
        # moon
        "moon": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" {extra}><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>',
        # sun
        "sun": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" {extra}><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>',
        # arrow right
        "arrow": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round" {extra}><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>',
        # clock / age
        "clock": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" {extra}><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>',
        # note / file
        "note": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" {extra}><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/><line x1="16" y1="13" x2="8" y2="13"/><line x1="16" y1="17" x2="8" y2="17"/><polyline points="10 9 9 9 8 9"/></svg>',
        # split / divide
        "split": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" {extra}><circle cx="18" cy="18" r="3"/><circle cx="6" cy="6" r="3"/><path d="M13 6h3a2 2 0 0 1 2 2v7"/><line x1="6" y1="9" x2="6" y2="21"/></svg>',
        # plus
        "plus": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" {extra}><line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/></svg>',
        # ledger / list
        "list": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" {extra}><line x1="8" y1="6" x2="21" y2="6"/><line x1="8" y1="12" x2="21" y2="12"/><line x1="8" y1="18" x2="21" y2="18"/><line x1="3" y1="6" x2="3.01" y2="6"/><line x1="3" y1="12" x2="3.01" y2="12"/><line x1="3" y1="18" x2="3.01" y2="18"/></svg>',
        # balance scale
        "scale": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" {extra}><line x1="12" y1="3" x2="12" y2="21"/><path d="M3 6l9-3 9 3"/><path d="M3 6c0 3.31 2.69 6 6 6s6-2.69 6-6"/><path d="M15 6c0 3.31 2.69 6 6 6s6-2.69 6-6" transform="translate(-6)"/><line x1="3" y1="21" x2="21" y2="21"/></svg>',
        # alert / warning
        "alert": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" {extra}><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>',
        # user / person
        "user": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" {extra}><path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/><circle cx="12" cy="7" r="4"/></svg>',
        # coins / money
        "coins": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" {extra}><circle cx="8" cy="8" r="6"/><path d="M18.09 10.37A6 6 0 1 1 10.34 18"/><path d="M7 6h1v4"/><line x1="16.71" y1="13.88" x2="13.91" y2="13.88"/></svg>',
        # empty inbox
        "inbox": f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round" {extra}><polyline points="22 12 16 12 14 15 10 15 8 12 2 12"/><path d="M5.45 5.11L2 12v6a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2v-6l-3.45-6.89A2 2 0 0 0 16.76 4H7.24a2 2 0 0 0-1.79 1.11z"/></svg>',
    }
    return paths.get(name, "")


# ── Avatar helpers ────────────────────────────────────────────────────────────
AVATAR_PALETTE = [
    ("#6366f1","#c7d2fe"), ("#8b5cf6","#ddd6fe"), ("#ec4899","#fbcfe8"),
    ("#14b8a6","#99f6e4"), ("#f59e0b","#fde68a"), ("#ef4444","#fecaca"),
    ("#06b6d4","#a5f3fc"), ("#10b981","#a7f3d0"),
]

def avatar_color(name):
    idx = int(hashlib.md5(name.lower().encode()).hexdigest(), 16) % len(AVATAR_PALETTE)
    return AVATAR_PALETTE[idx]

def initials(name):
    parts = name.strip().split()
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) >= 2 else name[:2].upper()

def debt_age(created_at):
    try:
        created = datetime.strptime(created_at, "%Y-%m-%d %H:%M:%S")
        days = (datetime.now() - created).days
        if days == 0:  return "today"
        if days == 1:  return "1 day ago"
        if days < 7:   return f"{days}d ago"
        if days < 30:  return f"{days}d ago"
        return f"{days}d ago"
    except:
        return ""

def whatsapp_link(from_p, to_p, amount, note):
    msg = f"hey {from_p}, quick reminder — you owe {to_p} {amount:.2f} AED"
    if note:
        msg += f" for {note}"
    return "https://wa.me/?text=" + urllib.parse.quote(msg)


# ── Theme state ───────────────────────────────────────────────────────────────
if "theme" not in st.session_state:
    st.session_state.theme = "dark"
if "confirm_delete" not in st.session_state:
    st.session_state.confirm_delete = None

D = st.session_state.theme == "dark"

BG         = "#080b14" if D else "#f4f6ff"
SURFACE    = "#111827" if D else "#ffffff"
SURFACE2   = "#1a2234" if D else "#f0f2ff"
SURFACE3   = "#0f1623" if D else "#e8ecff"
BORDER     = "rgba(255,255,255,0.07)" if D else "rgba(99,102,241,0.14)"
BORDER2    = "rgba(255,255,255,0.12)" if D else "rgba(99,102,241,0.25)"
TEXT       = "#f1f5ff" if D else "#1a1a3e"
TEXT2      = "rgba(241,245,255,0.38)" if D else "rgba(26,26,62,0.42)"
TEXT3      = "rgba(241,245,255,0.60)" if D else "rgba(26,26,62,0.62)"
ACCENT     = "#6366f1"
ACCENT_L   = "#818cf8"
ACCENT_D   = "#4f46e5"
POS        = "#34d399"
POS_BG     = "rgba(52,211,153,0.08)" if D else "rgba(52,211,153,0.10)"
POS_BORDER = "rgba(52,211,153,0.22)"
NEG        = "#f87171"
NEG_BG     = "rgba(248,113,113,0.08)" if D else "rgba(248,113,113,0.10)"
NEG_BORDER = "rgba(248,113,113,0.22)"
AMT_COLOR  = "#fbbf24"
AMT_BG     = "rgba(251,191,36,0.10)"
AMT_BORDER = "rgba(251,191,36,0.22)"
GLOW       = f"rgba(99,102,241,{'0.14' if D else '0.09'})"
INPUT_BG   = "rgba(255,255,255,0.04)" if D else "rgba(255,255,255,0.95)"
INPUT_BOR  = "rgba(255,255,255,0.10)" if D else "rgba(99,102,241,0.22)"
SHADOW     = f"rgba(0,0,0,{'0.45' if D else '0.10'})"
ICON_COL   = "rgba(241,245,255,0.35)" if D else "rgba(26,26,62,0.35)"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@500;700&display=swap');

*, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}

html, body, [data-testid="stAppViewContainer"] {{
    background: {BG};
    color: {TEXT};
    font-family: 'Outfit', sans-serif;
}}
[data-testid="stAppViewContainer"] {{
    background:
        radial-gradient(ellipse 80% 30% at 50% -5%, {GLOW}, transparent 60%),
        radial-gradient(ellipse 40% 20% at 85% 95%, rgba(99,102,241,0.05), transparent 60%),
        {BG};
    min-height: 100vh;
}}
[data-testid="stSidebar"], [data-testid="stHeader"], footer {{ display: none !important; }}
.block-container {{
    max-width: 680px !important;
    padding: 40px 20px 100px !important;
    margin: 0 auto !important;
}}

/* ── Logo ── */
.logo-wrap {{
    display: flex; align-items: flex-end; gap: 0; line-height: 1; margin-bottom: 4px;
}}
.logo-owe {{
    font-family: 'Outfit', sans-serif; font-size: clamp(38px, 8vw, 52px);
    font-weight: 900; color: {TEXT}; letter-spacing: -2px;
}}
.logo-no {{
    font-family: 'Outfit', sans-serif; font-size: clamp(38px, 8vw, 52px);
    font-weight: 900; letter-spacing: -2px;
    background: linear-gradient(135deg, {ACCENT}, {ACCENT_L} 60%, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}}
.logo-dot {{
    font-size: clamp(32px, 7vw, 46px); font-weight: 900;
    color: {ACCENT}; -webkit-text-fill-color: {ACCENT}; margin-left: 1px; padding-bottom: 4px;
}}
.hero-sub {{ font-size: 13px; color: {TEXT2}; margin-top: 3px; font-weight: 400; }}

/* ── Stats ── */
.stat-bar {{ display: flex; gap: 10px; margin: 26px 0 22px; }}
.stat-pill {{
    flex: 1; background: {SURFACE}; border: 1px solid {BORDER};
    border-radius: 18px; padding: 20px 10px 15px; text-align: center;
    box-shadow: 0 2px 20px {SHADOW}; position: relative; overflow: hidden;
}}
.stat-pill::before {{
    content: ''; position: absolute; top: 0; left: 15%; right: 15%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.5), transparent);
}}
.stat-icon {{ margin-bottom: 8px; opacity: 0.5; }}
.stat-num {{
    font-family: 'JetBrains Mono', monospace; font-size: 26px; font-weight: 700;
    background: linear-gradient(135deg, {ACCENT_L}, #a78bfa);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; line-height: 1;
}}
.stat-label {{
    font-size: 10px; color: {TEXT2}; text-transform: uppercase;
    letter-spacing: 2px; margin-top: 7px; font-weight: 700;
}}

/* ── Roast bar ── */
.roast-bar {{
    background: {SURFACE}; border: 1px solid {BORDER2};
    border-left: 3px solid {ACCENT}; border-radius: 12px;
    padding: 13px 18px; margin-bottom: 24px;
    font-size: 13px; color: {TEXT3}; font-style: italic; font-weight: 500; line-height: 1.5;
    display: flex; align-items: center; gap: 10px;
}}

/* ── Panel ── */
.panel {{
    background: {SURFACE}; border: 1px solid {BORDER}; border-radius: 24px;
    padding: 26px; margin-bottom: 18px; position: relative; overflow: hidden;
    box-shadow: 0 4px 40px {SHADOW};
}}
.panel::before {{
    content: ''; position: absolute; top: 0; left: 10%; right: 10%; height: 1px;
    background: linear-gradient(90deg, transparent, rgba(99,102,241,0.55), transparent);
}}
.panel-title {{
    font-size: 10px; font-weight: 700; letter-spacing: 3px;
    text-transform: uppercase; color: {TEXT2}; margin-bottom: 20px;
    display: flex; align-items: center; gap: 10px;
}}
.panel-title::after {{ content: ''; flex: 1; height: 1px; background: {BORDER}; }}

/* ── Debt item wrapper ── */
.debt-item-wrap {{ margin-bottom: 10px; }}

/* ── Debt card ── */
.debt-card {{
    display: flex; align-items: center; gap: 13px;
    background: {SURFACE2}; border: 1px solid {BORDER};
    border-radius: 16px; padding: 14px 16px;
    transition: all 0.2s cubic-bezier(0.4,0,0.2,1);
    position: relative; overflow: hidden;
}}
.debt-card::before {{
    content: ''; position: absolute; left: 0; top: 18%; bottom: 18%;
    width: 2px; background: linear-gradient(180deg, {ACCENT}, {ACCENT_L});
    border-radius: 0 2px 2px 0; opacity: 0.55;
}}
.debt-card:hover {{ border-color: {BORDER2}; box-shadow: 0 4px 20px {SHADOW}; }}

/* confirm-open state */
.debt-card.confirming {{
    border-color: rgba(248,113,113,0.3);
    border-bottom-left-radius: 0;
    border-bottom-right-radius: 0;
    border-bottom: none;
}}

.avatar {{
    width: 40px; height: 40px; border-radius: 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 800; flex-shrink: 0; letter-spacing: 0.3px;
}}
.debt-mid {{ flex: 1; min-width: 0; }}
.debt-names {{
    font-size: 14px; font-weight: 700; color: {TEXT};
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
    letter-spacing: -0.2px; display: flex; align-items: center; gap: 7px;
}}
.debt-arrow {{ opacity: 0.45; flex-shrink: 0; }}
.debt-meta {{ display: flex; align-items: center; gap: 7px; margin-top: 5px; flex-wrap: wrap; }}
.debt-note {{
    font-size: 12px; color: {TEXT2};
    overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    max-width: 180px; font-weight: 400;
    display: flex; align-items: center; gap: 4px;
}}
.age-badge {{
    font-size: 10px; color: {ACCENT_L};
    background: rgba(99,102,241,0.10); border-radius: 6px; padding: 2px 8px;
    font-weight: 600; white-space: nowrap;
    border: 1px solid rgba(99,102,241,0.18);
    font-family: 'JetBrains Mono', monospace;
    display: flex; align-items: center; gap: 4px;
}}
.debt-right {{ display: flex; align-items: center; gap: 10px; flex-shrink: 0; }}
.debt-amount {{
    font-family: 'JetBrains Mono', monospace; font-size: 14px; font-weight: 700;
    color: {AMT_COLOR}; background: {AMT_BG}; border: 1px solid {AMT_BORDER};
    border-radius: 9px; padding: 5px 11px; white-space: nowrap;
}}
.split-tag {{
    display: inline-flex; align-items: center; gap: 4px;
    background: rgba(99,102,241,0.12); border: 1px solid rgba(99,102,241,0.22);
    color: {ACCENT_L}; border-radius: 6px; padding: 2px 8px;
    font-size: 9px; font-weight: 800; letter-spacing: 1.5px; text-transform: uppercase;
}}

/* icon action buttons (pure HTML, not Streamlit buttons) */
.icon-btn {{
    width: 32px; height: 32px; border-radius: 9px; border: 1px solid {BORDER};
    background: transparent; display: flex; align-items: center; justify-content: center;
    cursor: pointer; transition: all 0.18s; flex-shrink: 0; text-decoration: none;
    color: {ICON_COL};
}}
.icon-btn:hover {{ background: {SURFACE3}; border-color: {BORDER2}; color: {TEXT}; }}
.icon-btn.danger:hover {{ background: {NEG_BG}; border-color: {NEG_BORDER}; color: {NEG}; }}

/* ── Inline confirm strip ── */
.confirm-strip {{
    background: {NEG_BG};
    border: 1px solid rgba(248,113,113,0.3);
    border-top: none;
    border-bottom-left-radius: 16px;
    border-bottom-right-radius: 16px;
    padding: 12px 16px;
    display: flex;
    align-items: center;
    gap: 12px;
}}
.confirm-strip-msg {{
    flex: 1; font-size: 12px; color: rgba(248,113,113,0.85); font-weight: 600;
    display: flex; align-items: center; gap: 7px;
}}
.confirm-strip-btns {{ display: flex; gap: 7px; flex-shrink: 0; }}
.cstrip-yes {{
    display: flex; align-items: center; gap: 5px;
    background: {NEG}; color: white; border: none;
    border-radius: 8px; padding: 6px 14px; font-size: 12px; font-weight: 700;
    cursor: pointer; transition: opacity 0.18s; font-family: 'Outfit', sans-serif;
    white-space: nowrap;
}}
.cstrip-yes:hover {{ opacity: 0.85; }}
.cstrip-no {{
    display: flex; align-items: center; gap: 5px;
    background: {SURFACE}; color: {TEXT3}; border: 1px solid {BORDER2};
    border-radius: 8px; padding: 6px 14px; font-size: 12px; font-weight: 600;
    cursor: pointer; transition: all 0.18s; font-family: 'Outfit', sans-serif;
    white-space: nowrap;
}}
.cstrip-no:hover {{ background: {SURFACE3}; }}

/* ── Balance grid ── */
.bal-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(140px, 1fr)); gap: 11px; }}
.bal-card {{
    border-radius: 18px; padding: 20px 14px 16px; text-align: center;
    border: 1px solid; position: relative; overflow: hidden; transition: transform 0.2s;
}}
.bal-card:hover {{ transform: translateY(-2px); }}
.bal-card::before {{
    content: ''; position: absolute; top: 0; left: 20%; right: 20%; height: 1px; opacity: 0.6;
}}
.bal-card.pos {{ background: {POS_BG}; border-color: {POS_BORDER}; }}
.bal-card.pos::before {{ background: linear-gradient(90deg, transparent, {POS}, transparent); }}
.bal-card.neg {{ background: {NEG_BG}; border-color: {NEG_BORDER}; }}
.bal-card.neg::before {{ background: linear-gradient(90deg, transparent, {NEG}, transparent); }}
.bal-card.zero {{ background: {SURFACE2}; border-color: {BORDER}; }}
.bal-avatar {{
    width: 40px; height: 40px; border-radius: 12px; margin: 0 auto 12px;
    display: flex; align-items: center; justify-content: center;
    font-size: 13px; font-weight: 800;
}}
.bal-name {{
    font-size: 12px; font-weight: 700; color: {TEXT3}; margin-bottom: 8px;
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}}
.bal-amount {{ font-family: 'JetBrains Mono', monospace; font-size: 20px; font-weight: 700; line-height: 1; }}
.bal-amount.pos {{ color: {POS}; }}
.bal-amount.neg {{ color: {NEG}; }}
.bal-amount.zero {{ color: {TEXT2}; }}
.bal-status {{
    font-size: 10px; margin-top: 6px; font-weight: 700;
    letter-spacing: 0.5px; text-transform: uppercase;
}}
.bal-status.pos {{ color: rgba(52,211,153,0.6); }}
.bal-status.neg {{ color: rgba(248,113,113,0.6); }}
.bal-status.zero {{ color: {TEXT2}; }}

/* ── Empty state ── */
.empty-state {{
    text-align: center; padding: 48px 16px;
    color: {TEXT2}; font-size: 13px; line-height: 1.8;
}}
.empty-icon {{ margin: 0 auto 16px; opacity: 0.3; width: fit-content; }}
.empty-title {{ font-size: 15px; font-weight: 600; color: {TEXT3}; margin-bottom: 6px; }}

/* ── Streamlit widget resets ── */
[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {{
    background: {INPUT_BG} !important; border: 1px solid {INPUT_BOR} !important;
    border-radius: 12px !important; color: {TEXT} !important;
    font-family: 'Outfit', sans-serif !important; font-size: 14px !important;
    font-weight: 500 !important; transition: border-color 0.2s, box-shadow 0.2s !important;
}}
[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {{
    border-color: {ACCENT} !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.14) !important; outline: none !important;
}}
[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label {{
    color: {TEXT2} !important; font-size: 11px !important; font-weight: 700 !important;
    letter-spacing: 2px !important; text-transform: uppercase !important;
    font-family: 'Outfit', sans-serif !important;
}}
[data-testid="stButton"] > button {{
    background: linear-gradient(135deg, {ACCENT} 0%, {ACCENT_D} 100%) !important;
    color: white !important; border: none !important; border-radius: 12px !important;
    font-family: 'Outfit', sans-serif !important; font-size: 14px !important;
    font-weight: 700 !important; letter-spacing: 0.3px !important;
    padding: 12px 20px !important; width: 100% !important;
    transition: all 0.2s !important; box-shadow: 0 4px 20px rgba(99,102,241,0.35) !important;
}}
[data-testid="stButton"] > button:hover {{
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 32px rgba(99,102,241,0.45) !important; filter: brightness(1.1) !important;
}}
[data-testid="stButton"] > button:active {{
    transform: translateY(0) !important; filter: brightness(0.97) !important;
}}

/* toggle button */
.toggle-btn [data-testid="stButton"] > button {{
    background: {SURFACE} !important; color: {TEXT} !important;
    border: 1px solid {BORDER2} !important; font-size: 14px !important;
    padding: 9px 13px !important; width: auto !important;
    box-shadow: none !important; border-radius: 12px !important; letter-spacing: 0 !important;
    display: flex; align-items: center; gap: 6px;
}}
.toggle-btn [data-testid="stButton"] > button:hover {{
    background: rgba(99,102,241,0.12) !important;
    border-color: rgba(99,102,241,0.35) !important;
    transform: none !important; box-shadow: none !important; filter: none !important;
}}

/* confirm strip Streamlit buttons */
.confirm-yes-btn [data-testid="stButton"] > button {{
    background: {NEG} !important;
    box-shadow: none !important; border-radius: 8px !important;
    padding: 7px 16px !important; font-size: 12px !important;
}}
.confirm-yes-btn [data-testid="stButton"] > button:hover {{
    opacity: 0.85 !important; transform: none !important;
    box-shadow: none !important; filter: none !important;
}}
.confirm-no-btn [data-testid="stButton"] > button {{
    background: {SURFACE} !important; color: {TEXT3} !important;
    border: 1px solid {BORDER2} !important; box-shadow: none !important;
    border-radius: 8px !important; padding: 7px 16px !important; font-size: 12px !important;
    filter: none !important;
}}
.confirm-no-btn [data-testid="stButton"] > button:hover {{
    background: {SURFACE3} !important; transform: none !important;
    box-shadow: none !important; filter: none !important;
}}

.stTabs [data-baseweb="tab-list"] {{
    background: {SURFACE2} !important; border-radius: 14px !important;
    padding: 5px !important; gap: 4px !important; border: 1px solid {BORDER} !important;
}}
.stTabs [data-baseweb="tab"] {{
    background: transparent !important; color: {TEXT2} !important;
    border-radius: 10px !important; font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important; font-size: 13px !important;
    padding: 8px 18px !important; transition: all 0.2s !important;
}}
.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {ACCENT}, {ACCENT_D}) !important;
    color: white !important; box-shadow: 0 2px 12px rgba(99,102,241,0.35) !important;
}}
.stTabs [data-baseweb="tab-panel"] {{ padding-top: 20px !important; }}

div[data-testid="column"] {{ padding: 0 4px !important; }}
div[data-testid="column"]:first-child {{ padding-left: 0 !important; }}
div[data-testid="column"]:last-child  {{ padding-right: 0 !important; }}
::-webkit-scrollbar {{ width: 4px; }}
::-webkit-scrollbar-thumb {{ background: rgba(99,102,241,0.25); border-radius: 4px; }}

@media (max-width: 480px) {{
    .stat-num {{ font-size: 22px; }}
    .bal-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .panel {{ padding: 18px; }}
    .debt-note {{ max-width: 110px; }}
}}
</style>
""", unsafe_allow_html=True)


# ── DB setup ──────────────────────────────────────────────────────────────────
conn = sqlite3.connect("oweno.db", check_same_thread=False)
c    = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS debts (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    from_person TEXT, to_person TEXT, amount REAL, note TEXT,
    created_at  TEXT, is_split INTEGER DEFAULT 0
)
""")
conn.commit()

existing_cols = [row[1] for row in c.execute("PRAGMA table_info(debts)").fetchall()]
now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
if "created_at" not in existing_cols:
    c.execute("ALTER TABLE debts ADD COLUMN created_at TEXT")
    c.execute("UPDATE debts SET created_at = ?", (now_str,))
    conn.commit()
if "is_split" not in existing_cols:
    c.execute("ALTER TABLE debts ADD COLUMN is_split INTEGER DEFAULT 0")
    c.execute("UPDATE debts SET is_split = 0")
    conn.commit()


# ── DB helpers ────────────────────────────────────────────────────────────────
def add_debt(f, t, a, n, is_split=0):
    c.execute(
        "INSERT INTO debts (from_person, to_person, amount, note, created_at, is_split) VALUES (?,?,?,?,?,?)",
        (f, t, a, n, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), is_split)
    )
    conn.commit()

def get_debts():
    return c.execute(
        "SELECT id, from_person, to_person, amount, note, created_at, is_split FROM debts ORDER BY id DESC"
    ).fetchall()

def delete_debt(i):
    c.execute("DELETE FROM debts WHERE id=?", (i,))
    conn.commit()

def get_balances():
    bal = {}
    for row in get_debts():
        _, f, t, a, *_ = row
        bal[f] = bal.get(f, 0) - a
        bal[t] = bal.get(t, 0) + a
    return bal

def get_roast(balances):
    if not balances: return None
    worst     = min(balances, key=balances.get)
    worst_val = balances[worst]
    if worst_val >= 0: return None
    roasts = [
        f"{worst} is down {abs(worst_val):.0f} AED — living on vibes and borrowed money.",
        f"{worst} owes {abs(worst_val):.0f} AED — wallet filed for emotional damage.",
        f"{worst} is {abs(worst_val):.0f} AED deep — the audacity to still be eating out.",
        f"Pour one out for {worst}. {abs(worst_val):.0f} AED lighter and still thriving (allegedly).",
        f"{worst} is the brokest one here at -{abs(worst_val):.0f} AED. Iconic.",
    ]
    idx = int(hashlib.md5(worst.encode()).hexdigest(), 16) % len(roasts)
    return roasts[idx]


# ── Data ──────────────────────────────────────────────────────────────────────
debts    = get_debts()
total    = c.execute("SELECT COALESCE(SUM(amount),0) FROM debts").fetchone()[0]
count    = c.execute("SELECT COUNT(*) FROM debts").fetchone()[0]
balances = get_balances()
roast    = get_roast(balances)


# ── Header ────────────────────────────────────────────────────────────────────
col_title, col_toggle = st.columns([6, 1])
with col_title:
    st.markdown("""
    <div class="logo-wrap">
        <span class="logo-owe">Owe</span><span class="logo-no">No</span><span class="logo-dot">.</span>
    </div>
    <div class="hero-sub">keeping friendships alive, one debt at a time</div>
    """, unsafe_allow_html=True)
with col_toggle:
    st.markdown('<div style="padding-top:8px" class="toggle-btn">', unsafe_allow_html=True)
    theme_icon = icon("moon", 15, "currentColor") if D else icon("sun", 15, "currentColor")
    if st.button(f"{'Dark' if not D else 'Light'}", key="theme_toggle"):
        st.session_state.theme = "light" if D else "dark"
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div style='margin-bottom:4px'></div>", unsafe_allow_html=True)


# ── Stats ─────────────────────────────────────────────────────────────────────
st.markdown(f"""
<div class="stat-bar">
  <div class="stat-pill">
    <div class="stat-icon">{icon("list", 18, ACCENT_L)}</div>
    <div class="stat-num">{count}</div>
    <div class="stat-label">Debts</div>
  </div>
  <div class="stat-pill">
    <div class="stat-icon">{icon("coins", 18, ACCENT_L)}</div>
    <div class="stat-num">{total:,.0f}</div>
    <div class="stat-label">Total AED</div>
  </div>
  <div class="stat-pill">
    <div class="stat-icon">{icon("user", 18, ACCENT_L)}</div>
    <div class="stat-num">{len(balances)}</div>
    <div class="stat-label">People</div>
  </div>
</div>
""", unsafe_allow_html=True)

if roast:
    st.markdown(f'<div class="roast-bar">{icon("alert", 15, ACCENT_L)}<span>{roast}</span></div>', unsafe_allow_html=True)


# ── Add debt panel ────────────────────────────────────────────────────────────
st.markdown(f'<div class="panel"><div class="panel-title">{icon("plus", 13, TEXT2)}Add a debt</div>', unsafe_allow_html=True)

tab_single, tab_split = st.tabs(["Single debt", "Split a bill"])

with tab_single:
    c1, c2 = st.columns(2)
    with c1:
        from_person = st.text_input("From — who owes", placeholder="Ahmed", key="s_from")
    with c2:
        to_person = st.text_input("To — who gets paid", placeholder="Sara", key="s_to")
    c3, c4 = st.columns([1, 2])
    with c3:
        amount = st.number_input("Amount (AED)", min_value=0.01, step=1.0, format="%.2f", key="s_amt")
    with c4:
        note = st.text_input("What for?", placeholder="dinner, petrol, concert", key="s_note")
    if st.button("Log debt", key="s_log"):
        if from_person.strip() and to_person.strip():
            if from_person.strip().lower() == to_person.strip().lower():
                st.error("A person can't owe themselves.")
            else:
                add_debt(from_person.strip(), to_person.strip(), amount, note.strip(), 0)
                st.success(f"{from_person} owes {to_person} {amount:.2f} AED — logged.")
                st.rerun()
        else:
            st.error("Fill in both names first.")

with tab_split:
    st.markdown(f'<div style="font-size:12px;color:{TEXT2};margin-bottom:16px;line-height:1.7">Enter who paid, the total, and who is splitting — each person owes an equal share.</div>', unsafe_allow_html=True)
    sp1, sp2 = st.columns([1, 1])
    with sp1:
        split_payer = st.text_input("Who paid?", placeholder="Sara", key="sp_payer")
    with sp2:
        split_total = st.number_input("Total bill (AED)", min_value=0.01, step=1.0, format="%.2f", key="sp_total")
    split_note  = st.text_input("What for?", placeholder="brunch, Airbnb, tickets", key="sp_note")
    split_names = st.text_input("Who's splitting? (comma separated)", placeholder="Ahmed, Khalid, Fatima, Omar", key="sp_names")
    if st.button("Split bill", key="sp_log"):
        people = [p.strip() for p in split_names.split(",") if p.strip()]
        people = [p for p in people if p.lower() != split_payer.strip().lower()]
        if not split_payer.strip():
            st.error("Who paid?")
        elif len(people) < 1:
            st.error("Add at least one person to split with.")
        else:
            per_person = split_total / (len(people) + 1)
            for person in people:
                add_debt(person, split_payer.strip(), round(per_person, 2), split_note.strip() or "split bill", 1)
            st.success(f"Split {split_total:.2f} AED — each person owes {per_person:.2f} AED to {split_payer}.")
            st.rerun()

st.markdown("</div>", unsafe_allow_html=True)


# ── Ledger ────────────────────────────────────────────────────────────────────
st.markdown(f'<div class="panel"><div class="panel-title">{icon("list", 13, TEXT2)}The ledger</div>', unsafe_allow_html=True)

if debts:
    for row in debts:
        id_, f, t, a, n, created_at, is_split = row
        age          = debt_age(created_at) if created_at else ""
        note_text    = n if n else "no note"
        av_bg, av_fg = avatar_color(f)
        av_init      = initials(f)
        is_confirming = st.session_state.confirm_delete == id_

        split_badge = (
            f'<span class="split-tag">{icon("split", 9, ACCENT_L)}split</span>'
            if is_split else ''
        )
        age_html = (
            f'<span class="age-badge">{icon("clock", 9, ACCENT_L)}{age}</span>'
            if age else ''
        )
        wa_url = whatsapp_link(f, t, a, n)

        card_class = "debt-card confirming" if is_confirming else "debt-card"

        # Debt card — pure HTML (no Streamlit columns around it so confirm strip attaches cleanly)
        st.markdown(f"""
        <div class="debt-item-wrap">
          <div class="{card_class}">
            <div class="avatar" style="background:{av_bg};color:{av_fg}">{av_init}</div>
            <div class="debt-mid">
              <div class="debt-names">
                <span>{f}</span>
                <span class="debt-arrow">{icon("arrow", 13, ICON_COL)}</span>
                <span>{t}</span>
                {split_badge}
              </div>
              <div class="debt-meta">
                <span class="debt-note">
                  {icon("note", 10, TEXT2)}
                  {note_text}
                </span>
                {age_html}
              </div>
            </div>
            <div class="debt-right">
              <div class="debt-amount">{a:,.2f} AED</div>
              <a href="{wa_url}" target="_blank" class="icon-btn" title="Send reminder">
                {icon("send", 14, ICON_COL)}
              </a>
            </div>
          </div>
        """, unsafe_allow_html=True)

        # ── Inline confirm strip (Streamlit buttons inside) ──────────────────
        if is_confirming:
            st.markdown(f"""
            <div class="confirm-strip">
              <div class="confirm-strip-msg">
                {icon("alert", 13, NEG)}
                Delete this debt? This cannot be undone.
              </div>
            </div>
            """, unsafe_allow_html=True)
            cy, cn = st.columns([1, 1])
            with cy:
                st.markdown('<div class="confirm-yes-btn">', unsafe_allow_html=True)
                if st.button("Delete", key=f"yes_{id_}"):
                    delete_debt(id_)
                    st.session_state.confirm_delete = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
            with cn:
                st.markdown('<div class="confirm-no-btn">', unsafe_allow_html=True)
                if st.button("Cancel", key=f"no_{id_}"):
                    st.session_state.confirm_delete = None
                    st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)
        else:
            # Delete trigger button — slim, below the card
            st.markdown('<div style="display:flex;justify-content:flex-end;margin-top:4px">', unsafe_allow_html=True)
            col_spacer, col_delbtn = st.columns([9, 1])
            with col_delbtn:
                if st.button(icon("trash", 13, NEG), key=f"del_{id_}", help="Delete debt"):
                    st.session_state.confirm_delete = id_
                    st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('</div>', unsafe_allow_html=True)  # close debt-item-wrap

else:
    st.markdown(f"""
    <div class="empty-state">
      <div class="empty-icon">{icon("inbox", 40, TEXT2)}</div>
      <div class="empty-title">Nothing here yet</div>
      No debts have been logged.<br>Add one above to get started.
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# ── Net balances ──────────────────────────────────────────────────────────────
if balances:
    st.markdown(f'<div class="panel"><div class="panel-title">{icon("scale", 13, TEXT2)}Net balances</div><div class="bal-grid">', unsafe_allow_html=True)
    for name, val in sorted(balances.items(), key=lambda x: x[1]):
        av_bg, av_fg = avatar_color(name)
        av_ini = initials(name)
        if val > 0.005:
            cls, amt_cls, status, sign = "pos", "pos", "is owed", "+"
        elif val < -0.005:
            cls, amt_cls, status, sign = "neg", "neg", "owes", ""
        else:
            cls, amt_cls, status, sign = "zero", "zero", "settled", ""
        st.markdown(f"""
        <div class="bal-card {cls}">
          <div class="bal-avatar" style="background:{av_bg};color:{av_fg}">{av_ini}</div>
          <div class="bal-name">{name}</div>
          <div class="bal-amount {amt_cls}">{sign}{abs(val):,.0f}</div>
          <div class="bal-status {amt_cls}">{status}</div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown("</div></div>", unsafe_allow_html=True)