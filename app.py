import streamlit as st
from datetime import date, timedelta

# ─── Page Config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Global CSS ─────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@300;400;600;700;800&display=swap');

/* ── Root Variables ── */
:root {
    --bg-primary: #0a0f1e;
    --bg-secondary: #0f1629;
    --bg-card: rgba(255,255,255,0.04);
    --bg-card-hover: rgba(255,255,255,0.07);
    --accent-blue: #4f8ef7;
    --accent-purple: #7c5cbf;
    --accent-teal: #00d4aa;
    --accent-orange: #ff7043;
    --accent-gold: #ffc107;
    --text-primary: #e8eaf6;
    --text-secondary: #9fa8da;
    --text-muted: #5c6bc0;
    --border: rgba(79,142,247,0.15);
    --border-hover: rgba(79,142,247,0.4);
    --radius: 16px;
    --radius-sm: 10px;
    --shadow: 0 8px 32px rgba(0,0,0,0.4);
    --shadow-glow: 0 0 40px rgba(79,142,247,0.15);
}

/* ── Base Overrides ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.main .block-container {
    padding: 0 !important;
    max-width: 100% !important;
}

/* ── Hide Streamlit Chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }

/* ── Body Background ── */
.stApp {
    background: linear-gradient(135deg, #0a0f1e 0%, #0f1a2e 40%, #0a1628 100%);
    min-height: 100vh;
}

/* ── Hero Section ── */
.hero-section {
    background: linear-gradient(135deg, #0d1b3e 0%, #1a0a2e 50%, #0a2040 100%);
    padding: 70px 60px 50px;
    position: relative;
    overflow: hidden;
    border-bottom: 1px solid var(--border);
}

.hero-section::before {
    content: '';
    position: absolute;
    top: -40%;
    right: -10%;
    width: 600px;
    height: 600px;
    background: radial-gradient(circle, rgba(79,142,247,0.12) 0%, transparent 70%);
    pointer-events: none;
}

.hero-section::after {
    content: '';
    position: absolute;
    bottom: -40%;
    left: -5%;
    width: 400px;
    height: 400px;
    background: radial-gradient(circle, rgba(124,92,191,0.1) 0%, transparent 70%);
    pointer-events: none;
}

.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: rgba(79,142,247,0.12);
    border: 1px solid rgba(79,142,247,0.3);
    color: #7eb8ff;
    padding: 6px 16px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    letter-spacing: 1.2px;
    text-transform: uppercase;
    margin-bottom: 20px;
}

.hero-title {
    font-family: 'Outfit', sans-serif;
    font-size: clamp(36px, 5vw, 64px);
    font-weight: 800;
    line-height: 1.1;
    background: linear-gradient(135deg, #e8eaf6 0%, #7eb8ff 40%, #a78bfa 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 18px;
}

.hero-subtitle {
    font-size: 17px;
    color: var(--text-secondary);
    line-height: 1.7;
    max-width: 600px;
    font-weight: 400;
}

.hero-stats {
    display: flex;
    gap: 40px;
    margin-top: 40px;
    flex-wrap: wrap;
}

.hero-stat {
    text-align: center;
}

.hero-stat-number {
    font-family: 'Outfit', sans-serif;
    font-size: 28px;
    font-weight: 800;
    background: linear-gradient(135deg, #4f8ef7, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-stat-label {
    font-size: 12px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 2px;
}

/* ── Section Wrapper ── */
.section-wrapper {
    padding: 40px 60px;
}

.section-title {
    font-family: 'Outfit', sans-serif;
    font-size: 22px;
    font-weight: 700;
    color: var(--text-primary);
    margin-bottom: 6px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-subtitle {
    font-size: 14px;
    color: var(--text-secondary);
    margin-bottom: 28px;
}

/* ── Card ── */
.glass-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 28px 32px;
    backdrop-filter: blur(20px);
    transition: all 0.3s ease;
    margin-bottom: 20px;
    box-shadow: var(--shadow);
}

.glass-card:hover {
    background: var(--bg-card-hover);
    border-color: var(--border-hover);
    box-shadow: var(--shadow-glow);
    transform: translateY(-2px);
}

/* ── Streamlit widget overrides ── */
div[data-testid="stTextInput"] > div > div > input,
div[data-testid="stDateInput"] > div > div > input,
div[data-testid="stNumberInput"] > div > div > input {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 14px !important;
    transition: border-color 0.3s ease !important;
}

div[data-testid="stTextInput"] > div > div > input:focus,
div[data-testid="stDateInput"] > div > div > input:focus,
div[data-testid="stNumberInput"] > div > div > input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 3px rgba(79,142,247,0.15) !important;
}

div[data-testid="stSelectbox"] > div > div,
div[data-testid="stMultiSelect"] > div > div {
    background: rgba(255,255,255,0.05) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
}

label[data-testid="stWidgetLabel"] > div > p {
    color: var(--text-secondary) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.3px !important;
}

/* ── Slider ── */
div[data-testid="stSlider"] > div {
    padding-top: 10px !important;
}

/* ── Purpose Buttons (radio style) ── */
.purpose-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 12px;
    margin-top: 10px;
    margin-bottom: 20px;
}

.purpose-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 16px 12px;
    text-align: center;
    cursor: pointer;
    transition: all 0.25s ease;
    position: relative;
}

.purpose-card:hover {
    background: rgba(79,142,247,0.1);
    border-color: var(--accent-blue);
}

.purpose-card.active {
    background: linear-gradient(135deg, rgba(79,142,247,0.2), rgba(124,92,191,0.2));
    border-color: var(--accent-blue);
    box-shadow: 0 0 20px rgba(79,142,247,0.2);
}

.purpose-icon { font-size: 26px; margin-bottom: 6px; }
.purpose-label { font-size: 12px; color: var(--text-secondary); font-weight: 600; }

/* ── Context Analysis Cards ── */
.context-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 16px;
    margin-top: 10px;
}

.context-chip {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 18px 20px;
    position: relative;
    overflow: hidden;
}

.context-chip::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    border-radius: var(--radius-sm) var(--radius-sm) 0 0;
}

.ctx-season::before { background: linear-gradient(90deg, #4f8ef7, #00d4aa); }
.ctx-budget::before { background: linear-gradient(90deg, #ffc107, #ff7043); }
.ctx-duration::before { background: linear-gradient(90deg, #a78bfa, #7c5cbf); }
.ctx-purpose::before { background: linear-gradient(90deg, #00d4aa, #4f8ef7); }

.context-chip-label {
    font-size: 11px;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-weight: 600;
    margin-bottom: 6px;
}

.context-chip-value {
    font-family: 'Outfit', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
}

.context-chip-sub {
    font-size: 12px;
    color: var(--text-secondary);
    margin-top: 2px;
}

/* ── Progress Steps ── */
.steps-bar {
    display: flex;
    align-items: center;
    gap: 0;
    margin-bottom: 36px;
    padding: 0 4px;
}

.step-item {
    display: flex;
    align-items: center;
    flex: 1;
}

.step-circle {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: 700;
    font-size: 13px;
    border: 2px solid;
    flex-shrink: 0;
    z-index: 1;
}

.step-circle.done {
    background: linear-gradient(135deg, #4f8ef7, #7c5cbf);
    border-color: transparent;
    color: white;
}

.step-circle.active {
    background: rgba(79,142,247,0.15);
    border-color: #4f8ef7;
    color: #4f8ef7;
    box-shadow: 0 0 0 4px rgba(79,142,247,0.1);
}

.step-circle.pending {
    background: rgba(255,255,255,0.03);
    border-color: rgba(255,255,255,0.1);
    color: #4a5568;
}

.step-connector {
    flex: 1;
    height: 2px;
    background: rgba(255,255,255,0.08);
    margin: 0 6px;
}

.step-connector.done {
    background: linear-gradient(90deg, #4f8ef7, #7c5cbf);
}

.step-label {
    font-size: 11px;
    text-align: center;
    margin-top: 6px;
    color: var(--text-muted);
    font-weight: 500;
}

.step-label.active { color: #4f8ef7; }
.step-label.done { color: #7c5cbf; }

/* ── Generate Button ── */
.stButton > button {
    background: linear-gradient(135deg, #4f8ef7 0%, #7c5cbf 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 16px 40px !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    font-family: 'Inter', sans-serif !important;
    letter-spacing: 0.5px !important;
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 8px 24px rgba(79,142,247,0.3) !important;
    width: 100% !important;
}

.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 12px 32px rgba(79,142,247,0.45) !important;
    filter: brightness(1.1) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Itinerary Day Cards ── */
.day-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 24px 28px;
    margin-bottom: 16px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}

.day-card:hover {
    border-color: var(--border-hover);
    transform: translateX(4px);
}

.day-card::before {
    content: '';
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, #4f8ef7, #7c5cbf);
    border-radius: 4px 0 0 4px;
}

.day-number {
    font-family: 'Outfit', sans-serif;
    font-size: 11px;
    font-weight: 700;
    color: #4f8ef7;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.day-title {
    font-family: 'Outfit', sans-serif;
    font-size: 18px;
    font-weight: 700;
    color: var(--text-primary);
    margin-top: 4px;
    margin-bottom: 12px;
}

.day-activity {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 8px;
}

.day-act-time {
    font-size: 11px;
    color: var(--text-muted);
    font-weight: 600;
    width: 55px;
    flex-shrink: 0;
    padding-top: 1px;
}

.day-act-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: #4f8ef7;
    margin-top: 5px;
    flex-shrink: 0;
}

.day-act-text {
    font-size: 13px;
    color: var(--text-secondary);
    line-height: 1.5;
}

/* ── Budget Indicator ── */
.budget-bar-wrap {
    background: rgba(255,255,255,0.05);
    border-radius: 999px;
    height: 8px;
    margin-top: 10px;
    overflow: hidden;
}

.budget-bar-fill {
    height: 100%;
    border-radius: 999px;
    transition: width 0.8s ease;
}

/* ── Tag Pills ── */
.tag-pill {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    background: rgba(79,142,247,0.12);
    border: 1px solid rgba(79,142,247,0.25);
    color: #7eb8ff;
    padding: 4px 12px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 600;
    margin-right: 6px;
    margin-bottom: 6px;
}

/* ── Divider ── */
.fancy-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(79,142,247,0.3), transparent);
    margin: 36px 0;
}

/* ── Info Banner ── */
.info-banner {
    background: linear-gradient(135deg, rgba(79,142,247,0.08), rgba(124,92,191,0.08));
    border: 1px solid rgba(79,142,247,0.2);
    border-radius: var(--radius-sm);
    padding: 16px 20px;
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 20px;
}

.info-banner-icon { font-size: 22px; }
.info-banner-text { font-size: 13px; color: var(--text-secondary); line-height: 1.5; }
.info-banner-strong { color: var(--text-primary); font-weight: 600; }

/* ── Responsive ── */
@media (max-width: 768px) {
    .hero-section { padding: 40px 24px 36px; }
    .section-wrapper { padding: 28px 24px; }
    .hero-stats { gap: 24px; }
}

/* ── Spinner override ── */
.stSpinner { color: var(--accent-blue) !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: rgba(79,142,247,0.3); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: rgba(79,142,247,0.6); }
</style>
""", unsafe_allow_html=True)


# ─── Helpers ────────────────────────────────────────────────────────────────────
def detect_season(travel_date: date) -> tuple[str, str]:
    month = travel_date.month
    if month in (12, 1, 2):
        return "❄️", "Winter"
    elif month in (3, 4, 5):
        return "🌸", "Spring"
    elif month in (6, 7, 8):
        return "☀️", "Summer"
    else:
        return "🍂", "Autumn"

def classify_budget(budget: float, duration: int) -> tuple[str, str, int]:
    if duration == 0:
        duration = 1
    daily = budget / duration
    if daily < 3000:
        return "🪙", "Budget Traveller", 25
    elif daily < 8000:
        return "💼", "Mid-Range Explorer", 55
    elif daily < 18000:
        return "✨", "Premium Comfort", 78
    else:
        return "💎", "Luxury Experience", 100

def get_purpose_color(purpose: str) -> str:
    colors = {
        "Adventure": "#ff7043",
        "Food & Cuisine": "#ffc107",
        "Scenic Beauty": "#00d4aa",
        "Culture & History": "#a78bfa",
        "Mixed Experience": "#4f8ef7",
    }
    return colors.get(purpose, "#4f8ef7")


# ─── Session State Defaults ──────────────────────────────────────────────────
if "step" not in st.session_state:
    st.session_state.step = 1
if "generated" not in st.session_state:
    st.session_state.generated = False


# ═══════════════════════════════════════════════════════════════════════════════
# HERO SECTION
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="hero-section">
    <div class="hero-badge">✨ AI-Powered · Context-Aware</div>
    <div class="hero-title">Your Smart Travel Planner</div>
    <div class="hero-subtitle">
        Discover personalized itineraries powered by contextual AI — tailored to your
        budget, travel purpose, season, and destination-specific insights.
    </div>
    <div class="hero-stats">
        <div class="hero-stat">
            <div class="hero-stat-number">500+</div>
            <div class="hero-stat-label">Destinations</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-number">98%</div>
            <div class="hero-stat-label">Satisfaction</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-number">6</div>
            <div class="hero-stat-label">Context Layers</div>
        </div>
        <div class="hero-stat">
            <div class="hero-stat-number">< 5s</div>
            <div class="hero-stat-label">Generation Time</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# PROGRESS STEPS
# ═══════════════════════════════════════════════════════════════════════════════
step = st.session_state.step

steps = ["Route Setup", "Dates & Budget", "Travel Style", "Generate"]

def step_class(i):
    n = i + 1
    if n < step:
        return "done"
    elif n == step:
        return "active"
    return "pending"

steps_html = '<div class="steps-bar">'
for i, s in enumerate(steps):
    cls = step_class(i)
    icon = "✓" if cls == "done" else str(i + 1)
    steps_html += f'<div style="display:flex;flex-direction:column;align-items:center;flex:1;">'
    steps_html += f'<div class="step-circle {cls}">{icon}</div>'
    steps_html += f'<div class="step-label {cls}">{s}</div>'
    steps_html += '</div>'
    if i < len(steps) - 1:
        conn_cls = "done" if step > i + 1 else ""
        steps_html += f'<div class="step-connector {conn_cls}" style="margin-bottom:18px;"></div>'
steps_html += '</div>'

st.markdown(f'<div class="section-wrapper">{steps_html}', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 1 — ROUTE SETUP
# ═══════════════════════════════════════════════════════════════════════════════
if step >= 1:
    st.markdown("""
        <div class="section-title">📍 Route Details</div>
        <div class="section-subtitle">Tell us where you're starting from and where you want to go</div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2, gap="large")

    with col1:
        origin = st.text_input(
            "📌 Starting Location",
            placeholder="e.g. Mumbai, Maharashtra",
            key="origin",
            help="Your departure city or airport"
        )

    with col2:
        destination = st.text_input(
            "🏔️ Destination",
            placeholder="e.g. Manali, Himachal Pradesh",
            key="destination",
            help="Where do you want to explore?"
        )

    checkpoints_raw = st.text_input(
        "🛣️ Optional Checkpoints",
        placeholder="e.g. Chandigarh → Shimla → Manali  (separate with →)",
        key="checkpoints",
        help="Add intermediate stops along the way (optional)"
    )

    if origin and destination:
        st.markdown(f"""
        <div class="info-banner">
            <span class="info-banner-icon">🗺️</span>
            <div class="info-banner-text">
                Route detected: <span class="info-banner-strong">{origin}</span>
                → {'→ '.join([c.strip() for c in checkpoints_raw.split('→') if c.strip()]+[destination]) if checkpoints_raw else destination}
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 2 — DATES & BUDGET
# ═══════════════════════════════════════════════════════════════════════════════
if step >= 2 or (st.session_state.get("origin") and st.session_state.get("destination")):
    st.markdown("""
        <div class="section-title">📅 Dates & Budget</div>
        <div class="section-subtitle">Set your travel window and total spending envelope</div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([2, 2, 1], gap="large")

    with col1:
        start_date = st.date_input(
            "🛫 Departure Date",
            value=date.today() + timedelta(days=14),
            min_value=date.today(),
            key="start_date"
        )

    with col2:
        end_date = st.date_input(
            "🛬 Return Date",
            value=date.today() + timedelta(days=21),
            min_value=date.today() + timedelta(days=1),
            key="end_date"
        )

    with col3:
        duration = (end_date - start_date).days if end_date > start_date else 1
        st.markdown(f"""
        <div style="padding-top:28px; text-align:center;">
            <div style="font-size:11px;color:#5c6bc0;text-transform:uppercase;letter-spacing:1px;font-weight:600;">Duration</div>
            <div style="font-family:'Outfit',sans-serif;font-size:34px;font-weight:800;
                        background:linear-gradient(135deg,#4f8ef7,#a78bfa);
                        -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                        background-clip:text;">{duration}</div>
            <div style="font-size:13px;color:#9fa8da;">day{'s' if duration != 1 else ''}</div>
        </div>
        """, unsafe_allow_html=True)

    # Budget slider
    budget = st.slider(
        "💰 Total Budget (INR ₹)",
        min_value=5000,
        max_value=500000,
        value=50000,
        step=1000,
        key="budget",
        format="₹%d"
    )

    b_icon, b_tier, b_pct = classify_budget(budget, duration)
    s_icon, s_name = detect_season(start_date)

    # Budget visualization
    col_a, col_b = st.columns([3, 1])
    with col_a:
        budget_color_map = {25: "#00d4aa", 55: "#4f8ef7", 78: "#a78bfa", 100: "#ffc107"}
        bar_color = budget_color_map.get(b_pct, "#4f8ef7")
        st.markdown(f"""
        <div style="margin-top:8px;">
            <div style="display:flex;justify-content:space-between;margin-bottom:6px;">
                <span style="font-size:13px;color:#9fa8da;">Budget Tier</span>
                <span style="font-size:13px;color:#e8eaf6;font-weight:600;">{b_icon} {b_tier}</span>
            </div>
            <div class="budget-bar-wrap">
                <div class="budget-bar-fill" style="width:{b_pct}%;background:linear-gradient(90deg,{bar_color},{bar_color}aa);"></div>
            </div>
            <div style="display:flex;justify-content:space-between;margin-top:5px;">
                <span style="font-size:11px;color:#5c6bc0;">₹{budget:,} total</span>
                <span style="font-size:11px;color:#5c6bc0;">≈ ₹{budget//duration:,}/day</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# STEP 3 — TRAVEL STYLE
# ═══════════════════════════════════════════════════════════════════════════════
if step >= 3 or True:
    st.markdown("""
        <div class="section-title">🎯 Travel Style & Preferences</div>
        <div class="section-subtitle">Shape the AI context engine to match your travel personality</div>
    """, unsafe_allow_html=True)

    # Purpose selection
    purposes = {
        "Adventure": "🧗",
        "Food & Cuisine": "🍜",
        "Scenic Beauty": "🌅",
        "Culture & History": "🏛️",
        "Mixed Experience": "✨",
    }

    selected_purpose = st.radio(
        "Primary Travel Purpose",
        options=list(purposes.keys()),
        horizontal=True,
        key="purpose",
        label_visibility="collapsed"
    )

    # Visual purpose cards
    purpose_cols = st.columns(len(purposes))
    for idx, (name, icon) in enumerate(purposes.items()):
        with purpose_cols[idx]:
            is_active = (selected_purpose == name)
            active_style = (
                "background:linear-gradient(135deg,rgba(79,142,247,0.2),rgba(124,92,191,0.2));"
                "border-color:#4f8ef7;"
                "box-shadow:0 0 20px rgba(79,142,247,0.2);"
            ) if is_active else ""
            color = get_purpose_color(name) if is_active else "transparent"
            st.markdown(f"""
            <div class="purpose-card {'active' if is_active else ''}" style="{active_style}">
                <div class="purpose-icon">{icon}</div>
                <div class="purpose-label" style="color:{'#e8eaf6' if is_active else '#9fa8da'};">{name}</div>
                {'<div style="width:6px;height:6px;border-radius:50%;background:'+color+';margin:6px auto 0;"></div>' if is_active else ''}
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)

    # Additional preferences
    col1, col2 = st.columns(2, gap="large")

    with col1:
        num_travelers = st.selectbox(
            "👥 Number of Travelers",
            options=["Solo (1)", "Couple (2)", "Small Group (3–5)", "Large Group (6+)", "Family with Kids"],
            key="travelers"
        )

        accommodation = st.selectbox(
            "🏨 Preferred Accommodation",
            options=["Hostels / Dorms", "Budget Hotels", "3-Star Hotels", "4-Star Hotels",
                     "5-Star / Luxury", "Boutique / Heritage", "Homestays / Airbnb"],
            key="accommodation"
        )

    with col2:
        transport = st.multiselect(
            "🚗 Preferred Transport",
            options=["Flight", "Train", "Bus", "Self-Drive / Rental Car", "Taxi / Cab", "Bike / Scooter"],
            default=["Flight", "Taxi / Cab"],
            key="transport"
        )

        interests = st.multiselect(
            "🎨 Specific Interests",
            options=["Photography", "Trekking / Hiking", "Wildlife Safaris", "Street Food", "Nightlife",
                     "Yoga & Wellness", "Water Sports", "Museums & Art", "Shopping", "Religious Sites"],
            default=["Photography"],
            key="interests"
        )

    dietary = st.radio(
        "🥗 Dietary Preferences",
        options=["No Restrictions", "Vegetarian", "Vegan", "Halal", "Gluten-Free"],
        horizontal=True,
        key="dietary"
    )

    st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# CONTEXT ANALYSIS DISPLAY
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown("""
    <div class="section-title">🧠 Context Intelligence</div>
    <div class="section-subtitle">AI-detected travel context based on your inputs</div>
""", unsafe_allow_html=True)

start_date_val = st.session_state.get("start_date", date.today() + timedelta(days=14))
end_date_val   = st.session_state.get("end_date",   date.today() + timedelta(days=21))
budget_val     = st.session_state.get("budget", 50000)
purpose_val    = st.session_state.get("purpose", "Mixed Experience")
duration_val   = max((end_date_val - start_date_val).days, 1)
s_icon_v, s_name_v = detect_season(start_date_val)
b_icon_v, b_tier_v, b_pct_v = classify_budget(budget_val, duration_val)
origin_val      = st.session_state.get("origin", "")
destination_val = st.session_state.get("destination", "")

context_html = f"""
<div class="context-grid">
    <div class="context-chip ctx-season">
        <div class="context-chip-label">Season Detected</div>
        <div class="context-chip-value">{s_icon_v} {s_name_v}</div>
        <div class="context-chip-sub">{start_date_val.strftime('%b %Y')}</div>
    </div>
    <div class="context-chip ctx-budget">
        <div class="context-chip-label">Budget Tier</div>
        <div class="context-chip-value">{b_icon_v} {b_tier_v}</div>
        <div class="context-chip-sub">₹{budget_val:,} · ₹{budget_val//duration_val:,}/day</div>
    </div>
    <div class="context-chip ctx-duration">
        <div class="context-chip-label">Trip Duration</div>
        <div class="context-chip-value">📆 {duration_val} Days</div>
        <div class="context-chip-sub">{start_date_val.strftime('%d %b')} → {end_date_val.strftime('%d %b %Y')}</div>
    </div>
    <div class="context-chip ctx-purpose">
        <div class="context-chip-label">Travel Purpose</div>
        <div class="context-chip-value">{purposes.get(purpose_val,'✨')} {purpose_val}</div>
        <div class="context-chip-sub">AI priority: {purpose_val.split()[0]} focus</div>
    </div>
</div>
"""
st.markdown(context_html, unsafe_allow_html=True)

st.markdown("<div style='height:24px'></div>", unsafe_allow_html=True)

# Active tags
tags_html = '<div style="margin-top:12px; margin-bottom:24px;">'
if origin_val:
    tags_html += f'<span class="tag-pill">📌 {origin_val}</span>'
if destination_val:
    tags_html += f'<span class="tag-pill">🏔️ {destination_val}</span>'
for t in st.session_state.get("transport", []):
    tags_html += f'<span class="tag-pill">🚗 {t}</span>'
for i in st.session_state.get("interests", []):
    tags_html += f'<span class="tag-pill">🎨 {i}</span>'
tags_html += f'<span class="tag-pill">🥗 {st.session_state.get("dietary","No Restrictions")}</span>'
tags_html += f'<span class="tag-pill">👥 {st.session_state.get("travelers","Solo (1)")}</span>'
tags_html += '</div>'
st.markdown(tags_html, unsafe_allow_html=True)

st.markdown('<div class="fancy-divider"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# GENERATE BUTTON
# ═══════════════════════════════════════════════════════════════════════════════
st.markdown('<div class="section-title">🚀 Generate Your Itinerary</div>', unsafe_allow_html=True)
st.markdown('<div class="section-subtitle">Our AI engine will craft a personalized day-by-day travel plan</div>', unsafe_allow_html=True)

can_generate = bool(origin_val and destination_val)

if not can_generate:
    st.markdown("""
    <div class="info-banner">
        <span class="info-banner-icon">⚠️</span>
        <div class="info-banner-text">
            Please fill in your <span class="info-banner-strong">Starting Location</span> and
            <span class="info-banner-strong">Destination</span> above to generate your itinerary.
        </div>
    </div>
    """, unsafe_allow_html=True)

col_btn, col_reset = st.columns([3, 1])
with col_btn:
    generate_clicked = st.button(
        "✨ Generate AI Travel Plan",
        disabled=not can_generate,
        use_container_width=True,
    )
with col_reset:
    reset_clicked = st.button(
        "🔄 Reset",
        use_container_width=True,
    )

if reset_clicked:
    for key in ["origin", "destination", "checkpoints", "generated"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

if generate_clicked and can_generate:
    st.session_state.generated = True

st.markdown('<div style="height:16px"></div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# ITINERARY RESULTS SECTION
# ═══════════════════════════════════════════════════════════════════════════════
if st.session_state.get("generated"):
    dest = destination_val or "Your Destination"
    orig = origin_val or "Your City"
    purpose_v = purpose_val
    dur_v     = duration_val

    with st.spinner("🧠 AI is analyzing destination data and crafting your itinerary..."):
        import time
        time.sleep(1.5)

    st.markdown(f"""
    <div style="background:linear-gradient(135deg,rgba(79,142,247,0.1),rgba(124,92,191,0.1));
                border:1px solid rgba(79,142,247,0.25);border-radius:16px;
                padding:28px 32px;margin-bottom:28px;">
        <div style="font-family:'Outfit',sans-serif;font-size:28px;font-weight:800;
                    background:linear-gradient(135deg,#e8eaf6,#7eb8ff,#a78bfa);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    background-clip:text;margin-bottom:6px;">
            🗺️ {dur_v}-Day {dest} Adventure
        </div>
        <div style="font-size:14px;color:#9fa8da;">
            {orig} → {dest} · {s_icon_v} {s_name_v} · {b_icon_v} {b_tier_v} · {purposes.get(purpose_v,'✨')} {purpose_v}
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Itinerary Tabs
    tab_labels = [f"Day {i+1}" for i in range(min(dur_v, 7))]
    tabs = st.tabs(tab_labels)

    sample_schedules = [
        [("07:00", "Arrival & hotel check-in, freshen up"),
         ("09:30", "Explore local market and street food breakfast"),
         ("12:00", "Visit the iconic downtown landmark"),
         ("15:00", "Afternoon scenic walk or photography session"),
         ("19:00", "Welcome dinner at a locally acclaimed restaurant"),
         ("21:30", "Stroll through the evening bazaar")],
        [("06:30", "Sunrise viewpoint trek (45 min)"),
         ("09:00", "Traditional breakfast at hilltop café"),
         ("11:00", "Adventure activity: Valley cable car ride"),
         ("13:30", "Packed lunch near the river bank"),
         ("15:00", "Cultural workshop or local craft experience"),
         ("18:30", "Bonfire & live folk music evening")],
        [("08:00", "Guided heritage walk through old city"),
         ("11:00", "Visit the famous museum or art gallery"),
         ("13:00", "Lunch at multi-cuisine rooftop restaurant"),
         ("15:30", "Shopping at curated local boutiques"),
         ("18:00", "Sunset boat ride or lake walk"),
         ("20:00", "Fine dining experience")],
    ]

    day_titles = [
        "Arrival & First Impressions", "Into the Wild", "Culture & Discovery",
        "Hidden Gems Day", "Adventure Peaks", "Leisure & Relaxation", "Fond Farewell"
    ]

    for i, tab in enumerate(tabs):
        with tab:
            sched = sample_schedules[i % len(sample_schedules)]
            title = day_titles[i % len(day_titles)]
            activities_html = ""
            for time_str, act in sched:
                activities_html += f"""
                <div class="day-activity">
                    <div class="day-act-time">{time_str}</div>
                    <div class="day-act-dot"></div>
                    <div class="day-act-text">{act}</div>
                </div>
                """
            st.markdown(f"""
            <div class="day-card">
                <div class="day-number">Day {i+1} of {dur_v}</div>
                <div class="day-title">{title}</div>
                {activities_html}
                <div style="margin-top:16px;padding-top:12px;border-top:1px solid rgba(255,255,255,0.06);
                            display:flex;gap:16px;">
                    <span style="font-size:12px;color:#5c6bc0;">💰 Est. ₹{(budget_val//dur_v):,}</span>
                    <span style="font-size:12px;color:#5c6bc0;">🌦️ {s_icon_v} {s_name_v} conditions</span>
                    <span style="font-size:12px;color:#5c6bc0;">{purposes.get(purpose_v,'✨')} {purpose_v} focus</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # Summary strip
    st.markdown(f"""
    <div style="background:var(--bg-card);border:1px solid var(--border);
                border-radius:var(--radius);padding:24px 28px;margin-top:20px;">
        <div style="font-family:'Outfit',sans-serif;font-size:18px;font-weight:700;
                    color:var(--text-primary);margin-bottom:16px;">📊 Trip Summary</div>
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:20px;">
            <div>
                <div style="font-size:11px;color:#5c6bc0;text-transform:uppercase;letter-spacing:1px;">Destination</div>
                <div style="font-size:16px;font-weight:700;color:#e8eaf6;margin-top:4px;">{dest}</div>
            </div>
            <div>
                <div style="font-size:11px;color:#5c6bc0;text-transform:uppercase;letter-spacing:1px;">Duration</div>
                <div style="font-size:16px;font-weight:700;color:#e8eaf6;margin-top:4px;">{dur_v} Days</div>
            </div>
            <div>
                <div style="font-size:11px;color:#5c6bc0;text-transform:uppercase;letter-spacing:1px;">Total Budget</div>
                <div style="font-size:16px;font-weight:700;color:#ffc107;margin-top:4px;">₹{budget_val:,}</div>
            </div>
            <div>
                <div style="font-size:11px;color:#5c6bc0;text-transform:uppercase;letter-spacing:1px;">Daily Budget</div>
                <div style="font-size:16px;font-weight:700;color:#00d4aa;margin-top:4px;">₹{budget_val//dur_v:,}</div>
            </div>
            <div>
                <div style="font-size:11px;color:#5c6bc0;text-transform:uppercase;letter-spacing:1px;">Season</div>
                <div style="font-size:16px;font-weight:700;color:#e8eaf6;margin-top:4px;">{s_icon_v} {s_name_v}</div>
            </div>
            <div>
                <div style="font-size:11px;color:#5c6bc0;text-transform:uppercase;letter-spacing:1px;">Travel Tier</div>
                <div style="font-size:16px;font-weight:700;color:#a78bfa;margin-top:4px;">{b_icon_v} {b_tier_v}</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;padding:40px 20px 30px;
            border-top:1px solid rgba(255,255,255,0.05);margin-top:40px;">
    <div style="font-size:24px;margin-bottom:8px;">✈️</div>
    <div style="font-family:'Outfit',sans-serif;font-size:16px;font-weight:700;
                background:linear-gradient(135deg,#4f8ef7,#a78bfa);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                background-clip:text;">AI Travel Planner</div>
    <div style="font-size:12px;color:#3a4563;margin-top:6px;">
        Context-Aware · Data-Grounded · Personalized
    </div>
</div>
""", unsafe_allow_html=True)
