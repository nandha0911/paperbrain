"""
frontend/styles.py
==================
Midnight Luxe & Glassmorphism design system for PaperBrain AI.
"""

CUSTOM_CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Global CSS Variables ── */
:root {
    --bg-canvas:       #0A0D14;
    --bg-card:         rgba(22, 27, 34, 0.7);
    --bg-card-hover:   rgba(30, 41, 59, 0.85);
    --border-subtle:   rgba(255, 255, 255, 0.08);
    --border-cyan:     rgba(6, 182, 212, 0.35);
    
    --accent-cyan:     #06B6D4;
    --accent-blue:     #3B82F6;
    --gradient-brand:  linear-gradient(135deg, #06B6D4 0%, #3B82F6 60%, #8B5CF6 100%);

    --text-primary:    #F8FAFC;
    --text-secondary:  #94A3B8;
    --text-muted:      #64748B;
    
    --font-heading:    'Plus Jakarta Sans', sans-serif;
    --font-body:       'Inter', sans-serif;
    --font-mono:       'JetBrains Mono', monospace;
    
    --radius-sm:       8px;
    --radius-md:       12px;
    --radius-lg:       16px;
    --radius-pill:     9999px;
    --transition:      all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── Global Canvas & Root Background ── */
html, body, #root, [data-testid="stAppViewContainer"], [data-testid="stMainBlockContainer"], [data-testid="stBottomBlockContainer"] {
    background-color: #0A0D14 !important;
    background: #0A0D14 !important;
    color: var(--text-primary) !important;
}

.stApp {
    background: 
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(6, 182, 212, 0.12), transparent),
        radial-gradient(ellipse 60% 40% at 100% 50%, rgba(139, 92, 246, 0.08), transparent),
        #0A0D14 !important;
    color: var(--text-primary) !important;
    min-height: 100vh !important;
}

/* ── Typography (Targeted to prevent breaking icons) ── */
h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-heading) !important;
    font-weight: 700 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.02em;
}

p, label, li {
    font-family: var(--font-body) !important;
    color: var(--text-primary) !important;
}

/* ── Clean Transparent Header & Sidebar Toggle Button ── */
header[data-testid="stHeader"] {
    background-color: transparent !important;
    background: transparent !important;
}

.stDeployButton, 
[data-testid="stDeployButton"],
footer,
#MainMenu {
    display: none !important;
}

[data-testid="stSidebarCollapseButton"] {
    display: block !important;
    visibility: visible !important;
}
[data-testid="stSidebarCollapseButton"] button {
    color: var(--text-primary) !important;
    background: rgba(22, 27, 34, 0.7) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
}
[data-testid="stSidebarCollapseButton"] button:hover {
    border-color: var(--accent-cyan) !important;
    color: var(--accent-cyan) !important;
}

/* ── Alerts & Warnings ── */
[data-testid="stAlert"] {
    background: rgba(30, 41, 59, 0.7) !important;
    border: 1px solid rgba(255, 255, 255, 0.1) !important;
    border-radius: var(--radius-sm) !important;
}
[data-testid="stAlert"] * {
    color: var(--text-primary) !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(13, 17, 23, 0.92) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-right: 1px solid var(--border-subtle) !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.25rem !important;
}

/* ── Sidebar Title ── */
.sidebar-title {
    font-family: var(--font-heading) !important;
    font-size: 1.4rem;
    font-weight: 800;
    background: var(--gradient-brand);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    display: flex;
    align-items: center;
    gap: 8px;
    letter-spacing: -0.03em;
    margin-bottom: 0.2rem;
}
.sidebar-subtitle {
    font-family: var(--font-body) !important;
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--text-muted) !important;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}

/* ── File Uploader Styling (Clean & Native) ── */
[data-testid="stFileUploader"] {
    background: transparent !important;
    margin-bottom: 1rem !important;
}
[data-testid="stFileUploader"] > section {
    background: rgba(22, 27, 34, 0.6) !important;
    border: 1px dashed var(--border-cyan) !important;
    border-radius: var(--radius-md) !important;
    padding: 1rem !important;
    transition: var(--transition) !important;
}
[data-testid="stFileUploader"] > section:hover {
    background: rgba(30, 41, 59, 0.85) !important;
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.15) !important;
}
[data-testid="stFileUploader"] small {
    color: var(--text-secondary) !important;
}

/* ── Document Cards ── */
.doc-card {
    background: rgba(22, 27, 34, 0.7);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 0.85rem 1rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: var(--transition);
}
.doc-card:hover {
    background: rgba(30, 41, 59, 0.9);
    border-color: var(--border-cyan);
    transform: translateY(-1px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
}
.doc-icon {
    font-size: 1.3rem;
    flex-shrink: 0;
}
.doc-info {
    display: flex;
    flex-direction: column;
    gap: 2px;
    overflow: hidden;
}
.doc-name {
    font-family: var(--font-heading);
    font-weight: 600;
    font-size: 0.85rem;
    color: var(--text-primary);
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.doc-meta {
    font-family: var(--font-body);
    font-size: 0.72rem;
    color: var(--text-secondary);
}

/* ── Expanders (Settings) ── */
[data-testid="stExpander"] {
    background: rgba(22, 27, 34, 0.5) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-md) !important;
    overflow: hidden !important;
}
[data-testid="stExpander"] summary {
    color: var(--text-primary) !important;
    font-family: var(--font-heading) !important;
    font-weight: 600 !important;
    font-size: 0.88rem !important;
}
[data-testid="stExpander"] summary:hover {
    color: var(--accent-cyan) !important;
}

/* ── Hero Welcome Card ── */
.hero-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 3rem 1.5rem;
    text-align: center;
    max-width: 680px;
    margin: 1.5rem auto;
    background: rgba(17, 24, 39, 0.4);
    border: 1px solid var(--border-subtle);
    border-radius: 20px;
    backdrop-filter: blur(16px);
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
}
.hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    background: rgba(6, 182, 212, 0.1);
    border: 1px solid rgba(6, 182, 212, 0.3);
    border-radius: var(--radius-pill);
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--accent-cyan);
    margin-bottom: 1.25rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.hero-title {
    font-family: var(--font-heading);
    font-size: 2.2rem;
    font-weight: 800;
    color: #FFFFFF;
    letter-spacing: -0.03em;
    margin-bottom: 0.75rem;
    line-height: 1.2;
}
.hero-title span {
    background: var(--gradient-brand);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-desc {
    font-family: var(--font-body);
    font-size: 0.95rem;
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 2rem;
}
.hero-chips-grid {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    justify-content: center;
}
.hero-chip {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-pill);
    padding: 8px 16px;
    font-size: 0.8rem;
    font-weight: 500;
    color: var(--text-secondary);
    transition: var(--transition);
    display: flex;
    align-items: center;
    gap: 6px;
}
.hero-chip:hover {
    background: rgba(6, 182, 212, 0.1);
    border-color: var(--accent-cyan);
    color: var(--text-primary);
    transform: translateY(-2px);
}

/* ── Chat Messages ── */
.message-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.25rem;
    padding: 1rem 1.25rem;
    border-radius: var(--radius-md);
    background: rgba(17, 24, 39, 0.6);
    border: 1px solid var(--border-subtle);
    backdrop-filter: blur(12px);
}
.message-row.user {
    background: rgba(30, 41, 59, 0.55);
    border-color: rgba(255, 255, 255, 0.08);
}
.bubble {
    font-family: var(--font-body);
    font-size: 0.95rem;
    line-height: 1.7;
    color: var(--text-primary);
}
.avatar {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.avatar-user {
    background: var(--accent-blue);
    color: white;
}
.avatar-bot {
    background: var(--gradient-brand);
    color: white;
}
.msg-meta {
    font-size: 0.7rem;
    color: var(--text-muted);
    margin-top: 4px;
}

/* ── Fix Bottom Bar White Background ── */
[data-testid="stBottom"],
.stBottom,
div[data-testid="stBottom"] > div,
[data-testid="stBottom"] * {
    background-color: transparent !important;
}

/* ── Unified Single Floating Chat Input ── */
.stChatInput {
    padding-bottom: 1.5rem !important;
}
[data-testid="stChatInput"] > div {
    background: rgba(17, 24, 39, 0.85) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.14) !important;
    border-radius: var(--radius-lg) !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5) !important;
    transition: var(--transition) !important;
}
[data-testid="stChatInput"] > div:focus-within {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 24px rgba(6, 182, 212, 0.25) !important;
}
[data-testid="stChatInput"] textarea {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 0.95rem !important;
}
[data-testid="stChatInput"] button {
    background: transparent !important;
    color: var(--accent-cyan) !important;
    border: none !important;
}

/* ── Buttons ── */
.stButton > button {
    background: rgba(255, 255, 255, 0.05) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-heading) !important;
    font-weight: 600 !important;
    transition: var(--transition) !important;
}
.stButton > button:hover {
    background: rgba(255, 255, 255, 0.1) !important;
    border-color: var(--accent-cyan) !important;
    color: var(--accent-cyan) !important;
    transform: translateY(-1px);
}
.stButton > button[kind="primary"] {
    background: var(--gradient-brand) !important;
    color: #FFFFFF !important;
    border: none !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.4) !important;
}

</style>
"""

# ── Hero Welcome Screen ───────────────────────────────────────────────────────
WELCOME_PANEL_HTML = """
<div class="hero-container">
    <div class="hero-badge">⚡ Neural Document Intelligence</div>
    <div class="hero-title">Ask <span>PaperBrain</span></div>
    <div class="hero-desc">
        Upload your PDF documents and ask anything. Grounded strictly in your data with exact source citations and zero hallucinations.
    </div>
    <div class="hero-chips-grid">
        <div class="hero-chip">🔍 Hybrid Vector Search</div>
        <div class="hero-chip">📑 Exact Page Citations</div>
        <div class="hero-chip">⚡ Powered by Gemini Flash</div>
    </div>
</div>
"""

# ── Typing Indicator ──────────────────────────────────────────────────────────
TYPING_INDICATOR_HTML = """
<div style="display: flex; align-items: center; gap: 0.75rem; padding: 1rem 0;">
    <div style="width: 32px; height: 32px; border-radius: 8px; background: linear-gradient(135deg, #06B6D4, #3B82F6); color: white; display: flex; align-items: center; justify-content: center; font-size: 1rem;">🧠</div>
    <div style="display: flex; gap: 4px; align-items: center;">
        <div style="width: 6px; height: 6px; background: #06B6D4; border-radius: 50%; animation: typingDot 1.4s ease-in-out infinite;"></div>
        <div style="width: 6px; height: 6px; background: #06B6D4; border-radius: 50%; animation: typingDot 1.4s ease-in-out 0.2s infinite;"></div>
        <div style="width: 6px; height: 6px; background: #06B6D4; border-radius: 50%; animation: typingDot 1.4s ease-in-out 0.4s infinite;"></div>
    </div>
</div>
<style>
@keyframes typingDot {
    0%, 60%, 100% { opacity: 0.3; transform: scale(0.8); }
    30% { opacity: 1; transform: scale(1.2); }
}
</style>
"""
