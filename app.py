import streamlit as st
import sqlite3

st.set_page_config(page_title="Who Owes Who 💸", layout="centered", page_icon="💸")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;1,400&family=JetBrains+Mono:wght@500;700&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

html, body, [data-testid="stAppViewContainer"] {
    background: #0c0e14;
    color: #e2e4ed;
    font-family: 'DM Sans', sans-serif;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 70% 40% at 50% 0%, rgba(250,204,21,0.07) 0%, transparent 65%),
        #0c0e14;
}

[data-testid="stSidebar"], [data-testid="stHeader"] { display: none !important; }

.block-container {
    max-width: 680px !important;
    padding: 36px 20px 80px !important;
    margin: 0 auto !important;
}

.hero {
    text-align: center;
    margin-bottom: 40px;
}

.hero-emoji {
    font-size: 48px;
    display: block;
    margin-bottom: 8px;
    animation: float 3s ease-in-out infinite;
}

@keyframes float {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-8px); }
}

.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(44px, 10vw, 72px);
    letter-spacing: 3px;
    color: #facc15;
    text-shadow: 0 0 40px rgba(250,204,21,0.3);
    line-height: 1;
}

.hero-sub {
    font-size: 13px;
    color: rgba(255,255,255,0.3);
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-top: 6px;
    font-style: italic;
}

.stat-row {
    display: flex;
    gap: 10px;
    margin-bottom: 32px;
}

.stat-pill {
    flex: 1;
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 12px;
    padding: 14px 16px;
    text-align: center;
}

.stat-pill-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 20px;
    font-weight: 700;
    color: #facc15;
}

.stat-pill-label {
    font-size: 10px;
    color: rgba(255,255,255,0.28);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 3px;
}

.panel {
    background: rgba(255,255,255,0.025);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}

.panel::before {
    content: '';
    position: absolute;
    top: 0; left: 10%; right: 10%;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(250,204,21,0.35), transparent);
}

.panel-title {
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.28);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.debt-item {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: rgba(255,255,255,0.02);
    border: 1px solid rgba(255,255,255,0.055);
    border-radius: 11px;
    padding: 14px 16px;
    margin-bottom: 8px;
    transition: background 0.15s, border-color 0.15s;
    gap: 10px;
}

.debt-item:hover {
    background: rgba(255,255,255,0.04);
    border-color: rgba(255,255,255,0.09);
}

.debt-item-left { flex: 1; min-width: 0; }

.debt-who {
    font-size: 14px;
    font-weight: 500;
    color: #e2e4ed;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.debt-who b { color: #facc15; }

.debt-note {
    font-size: 11px;
    color: rgba(255,255,255,0.25);
    margin-top: 3px;
    font-style: italic;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.debt-right {
    display: flex;
    align-items: center;
    gap: 12px;
    flex-shrink: 0;
}

.debt-amount {
    font-family: 'JetBrains Mono', monospace;
    font-size: 16px;
    font-weight: 700;
    color: #facc15;
    white-space: nowrap;
}

.bal-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(140px, 1fr));
    gap: 10px;
}

.bal-card {
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    border: 1px solid;
}

.bal-card.pos {
    background: rgba(74,222,128,0.05);
    border-color: rgba(74,222,128,0.2);
}

.bal-card.neg {
    background: rgba(248,113,113,0.05);
    border-color: rgba(248,113,113,0.2);
}

.bal-card.zero {
    background: rgba(255,255,255,0.03);
    border-color: rgba(255,255,255,0.07);
}

.bal-name {
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: rgba(255,255,255,0.5);
    margin-bottom: 8px;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}

.bal-amount {
    font-family: 'JetBrains Mono', monospace;
    font-size: 20px;
    font-weight: 700;
}

.bal-amount.pos { color: #4ade80; }
.bal-amount.neg { color: #f87171; }
.bal-amount.zero { color: rgba(255,255,255,0.3); }

.bal-status {
    font-size: 10px;
    margin-top: 5px;
    letter-spacing: 0.5px;
}

.bal-status.pos { color: rgba(74,222,128,0.45); }
.bal-status.neg { color: rgba(248,113,113,0.45); }
.bal-status.zero { color: rgba(255,255,255,0.2); }

.empty-state {
    text-align: center;
    padding: 32px 16px;
    color: rgba(255,255,255,0.18);
    font-size: 13px;
    font-style: italic;
}

.empty-emoji { font-size: 32px; display: block; margin-bottom: 8px; }

[data-testid="stTextInput"] input,
[data-testid="stNumberInput"] input {
    background: rgba(255,255,255,0.04) !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 10px !important;
    color: #e2e4ed !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    transition: border-color 0.2s, box-shadow 0.2s !important;
}

[data-testid="stTextInput"] input:focus,
[data-testid="stNumberInput"] input:focus {
    border-color: rgba(250,204,21,0.45) !important;
    box-shadow: 0 0 0 3px rgba(250,204,21,0.07) !important;
}

[data-testid="stTextInput"] label,
[data-testid="stNumberInput"] label {
    color: rgba(255,255,255,0.38) !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
}

[data-testid="stButton"] > button {
    background: #facc15 !important;
    color: #0c0e14 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 14px !important;
    font-weight: 700 !important;
    letter-spacing: 1px !important;
    padding: 11px 20px !important;
    width: 100% !important;
    text-transform: uppercase !important;
    transition: all 0.18s !important;
}

[data-testid="stButton"] > button:hover {
    background: #fde047 !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(250,204,21,0.28) !important;
}

[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

.del-wrap [data-testid="stButton"] > button {
    background: transparent !important;
    color: rgba(248,113,113,0.5) !important;
    border: 1px solid rgba(248,113,113,0.15) !important;
    font-size: 14px !important;
    padding: 6px 10px !important;
    width: auto !important;
    letter-spacing: 0 !important;
    text-transform: none !important;
    font-weight: 400 !important;
}

.del-wrap [data-testid="stButton"] > button:hover {
    color: #f87171 !important;
    border-color: rgba(248,113,113,0.4) !important;
    background: rgba(248,113,113,0.07) !important;
    transform: none !important;
    box-shadow: none !important;
}

div[data-testid="column"] { padding: 0 5px !important; }
div[data-testid="column"]:first-child { padding-left: 0 !important; }
div[data-testid="column"]:last-child { padding-right: 0 !important; }

::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.08); border-radius: 3px; }

@media (max-width: 480px) {
    .stat-row { gap: 8px; }
    .stat-pill-num { font-size: 16px; }
    .bal-grid { grid-template-columns: repeat(2, 1fr); }
    .panel { padding: 18px; }
}
</style>
""", unsafe_allow_html=True)

conn = sqlite3.connect("debts.db", check_same_thread=False)
c = conn.cursor()
c.execute("""
CREATE TABLE IF NOT EXISTS debts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    from_person TEXT,
    to_person TEXT,
    amount REAL,
    note TEXT
)
""")
conn.commit()

def add_debt(f, t, a, n):
    c.execute("INSERT INTO debts (from_person, to_person, amount, note) VALUES (?, ?, ?, ?)", (f, t, a, n))
    conn.commit()

def get_debts():
    return c.execute("SELECT * FROM debts ORDER BY id DESC").fetchall()

def delete_debt(i):
    c.execute("DELETE FROM debts WHERE id=?", (i,))
    conn.commit()

def get_balances():
    rows = get_debts()
    bal = {}
    for _, f, t, a, _ in rows:
        bal[f] = bal.get(f, 0) - a
        bal[t] = bal.get(t, 0) + a
    return bal

def get_total():
    r = c.execute("SELECT COALESCE(SUM(amount),0) FROM debts").fetchone()
    return r[0]

def get_count():
    r = c.execute("SELECT COUNT(*) FROM debts").fetchone()
    return r[0]

def get_roast(balances):
    if not balances:
        return None
    worst = min(balances, key=balances.get)
    worst_val = balances[worst]
    if worst_val >= 0:
        return None
    roasts = [
        f"👀 {worst} is down {abs(worst_val):.0f} AED. bro is eating ramen in a Ferrari.",
        f"💀 {worst} owes {abs(worst_val):.0f} AED. their wallet filed for emotional damage.",
        f"😭 {worst} is {abs(worst_val):.0f} AED deep. the audacity to still be eating out.",
        f"🫡 pour one out for {worst}. {abs(worst_val):.0f} AED lighter and still thriving (allegedly).",
        f"🚨 {worst} is the most broke person here at -{abs(worst_val):.0f} AED. classic.",
    ]
    import hashlib
    idx = int(hashlib.md5(worst.encode()).hexdigest(), 16) % len(roasts)
    return roasts[idx]

debts = get_debts()
total = get_total()
count = get_count()
balances = get_balances()
roast = get_roast(balances)

st.markdown("""
<div class="hero">
    <span class="hero-emoji">💸</span>
    <div class="hero-title">Who Owes Who</div>
    <div class="hero-sub">keeping friendships alive, one debt at a time</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""
<div class="stat-row">
    <div class="stat-pill">
        <div class="stat-pill-num">{count}</div>
        <div class="stat-pill-label">Active debts</div>
    </div>
    <div class="stat-pill">
        <div class="stat-pill-num">{total:,.0f}</div>
        <div class="stat-pill-label">Total AED</div>
    </div>
    <div class="stat-pill">
        <div class="stat-pill-num">{len(balances)}</div>
        <div class="stat-pill-label">People involved</div>
    </div>
</div>
""", unsafe_allow_html=True)

if roast:
    st.markdown(f"""
    <div style="background:rgba(250,204,21,0.05);border:1px solid rgba(250,204,21,0.14);border-radius:12px;padding:13px 18px;margin-bottom:24px;font-size:13px;color:rgba(255,255,255,0.6);font-style:italic;text-align:center;">
        {roast}
    </div>
    """, unsafe_allow_html=True)

st.markdown("""
<div class="panel">
    <div class="panel-title">➕ &nbsp;Add a debt</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    from_person = st.text_input("From — who owes", placeholder="Ahmed")
with col2:
    to_person = st.text_input("To — who gets paid", placeholder="Sara")

col3, col4 = st.columns([1.2, 2])
with col3:
    amount = st.number_input("Amount (AED)", min_value=0.01, step=1.0, format="%.2f")
with col4:
    note = st.text_input("What for?", placeholder="dinner, petrol, that thing…")

if st.button("Log it 📝"):
    if from_person.strip() and to_person.strip():
        if from_person.strip().lower() == to_person.strip().lower():
            st.error("Can't owe yourself bro 😭")
        else:
            add_debt(from_person.strip(), to_person.strip(), amount, note.strip())
            st.success(f"Noted! {from_person} now owes {to_person} {amount:.2f} AED 💀")
            st.rerun()
    else:
        st.error("Fill in both names first!")

st.markdown("</div>", unsafe_allow_html=True)

st.markdown("""
<div class="panel">
    <div class="panel-title">📋 &nbsp;The ledger</div>
""", unsafe_allow_html=True)

if debts:
    for d in debts:
        id_, f, t, a, n = d
        col_info, col_del = st.columns([9, 1])
        with col_info:
            note_text = n if n else "no reason given (suspicious 👀)"
            st.markdown(f"""
            <div class="debt-item">
                <div class="debt-item-left">
                    <div class="debt-who"><b>{f}</b> → <b>{t}</b></div>
                    <div class="debt-note">{note_text}</div>
                </div>
                <div class="debt-right">
                    <div class="debt-amount">{a:,.2f} AED</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_del:
            st.markdown('<div class="del-wrap" style="padding-top:8px">', unsafe_allow_html=True)
            if st.button("✕", key=f"del_{id_}"):
                delete_debt(id_)
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("""
    <div class="empty-state">
        <span class="empty-emoji">🎉</span>
        nobody owes anybody anything. friendship saved.
    </div>
    """, unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

if balances:
    st.markdown("""
    <div class="panel">
        <div class="panel-title">⚖️ &nbsp;Net balances</div>
    <div class="bal-grid">
    """, unsafe_allow_html=True)

    for name, val in sorted(balances.items(), key=lambda x: x[1]):
        if val > 0:
            cls, amt_cls = "pos", "pos"
            status = "is owed 🤑"
        elif val < 0:
            cls, amt_cls = "neg", "neg"
            status = "owes people 😬"
        else:
            cls, amt_cls = "zero", "zero"
            status = "all settled ✅"

        sign = "+" if val > 0 else ""
        st.markdown(f"""
        <div class="bal-card {cls}">
            <div class="bal-name">{name}</div>
            <div class="bal-amount {amt_cls}">{sign}{val:,.0f}</div>
            <div class="bal-status {amt_cls}">{status}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("</div></div>", unsafe_allow_html=True)