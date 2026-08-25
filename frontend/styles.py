"""
frontend/styles.py
==================
Midnight Luxe & Glassmorphism design system for PaperBrain AI.
"""

CUSTOM_CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700;800&family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Design System Variables ── */
:root {
    --bg-canvas:       #0A0D14;
    --bg-surface:      rgba(17, 24, 39, 0.75);
    --bg-card:         rgba(22, 27, 34, 0.65);
    --bg-card-hover:   rgba(30, 41, 59, 0.85);
    --border-subtle:   rgba(255, 255, 255, 0.08);
    --border-glow:     rgba(6, 182, 212, 0.4);
    
    --accent-cyan:     #06B6D4;
    --accent-blue:     #3B82F6;
    --accent-emerald:  #10B981;
    --gradient-brand:  linear-gradient(135deg, #06B6D4 0%, #3B82F6 50%, #8B5CF6 100%);
    --gradient-glow:   radial-gradient(circle at 50% 0%, rgba(6, 182, 212, 0.15), transparent 70%);

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

/* ── Global Canvas ── */
html, body, [class*="css"] {
    font-family: var(--font-body) !important;
    background-color: var(--bg-canvas) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background: 
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(6, 182, 212, 0.12), transparent),
        radial-gradient(ellipse 60% 40% at 100% 50%, rgba(139, 92, 246, 0.08), transparent),
        #0A0D14 !important;
    color: var(--text-primary) !important;
}

/* ── Protect Material Icons ── */
[data-testid="stIconMaterial"], 
.material-symbols-rounded,
[class*="material-symbols"],
[data-testid="stSidebarCollapseButton"] * {
    font-family: 'Material Symbols Rounded', sans-serif !important;
}

/* ── Hide Streamlit default Deploy button & footer ── */
.stDeployButton, 
[data-testid="stDeployButton"],
footer, 
header[data-testid="stHeader"] {
    display: none !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: rgba(13, 17, 23, 0.85) !important;
    backdrop-filter: blur(20px) !important;
    -webkit-backdrop-filter: blur(20px) !important;
    border-right: 1px solid var(--border-subtle) !important;
    box-shadow: 4px 0 24px rgba(0, 0, 0, 0.4) !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.25rem !important;
}

/* Force dark sidebar text */
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label {
    color: var(--text-primary) !important;
    font-family: var(--font-heading) !important;
}
[data-testid="stSidebar"] hr {
    border-top: 1px solid var(--border-subtle) !important;
    margin: 1.25rem 0 !important;
}

/* ── Sidebar Title ── */
.sidebar-title {
    font-family: var(--font-heading) !important;
    font-size: 1.35rem;
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

/* ── Modern File Uploader Dropzone ── */
[data-testid="stFileUploader"] {
    background: transparent !important;
}
[data-testid="stFileUploadDropzone"] {
    background: rgba(22, 27, 34, 0.5) !important;
    border: 1px dashed rgba(6, 182, 212, 0.3) !important;
    border-radius: var(--radius-md) !important;
    padding: 1.25rem 1rem !important;
    transition: var(--transition) !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    border-color: var(--accent-cyan) !important;
    background: rgba(30, 41, 59, 0.7) !important;
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.15) !important;
}
[data-testid="stFileUploadDropzone"] button {
    background: rgba(255, 255, 255, 0.08) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-body) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    transition: var(--transition) !important;
}
[data-testid="stFileUploadDropzone"] button:hover {
    background: var(--accent-cyan) !important;
    color: #0A0D14 !important;
    border-color: var(--accent-cyan) !important;
}

/* ── Document Cards ── */
.doc-card {
    background: rgba(22, 27, 34, 0.6);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius-md);
    padding: 0.85rem 1rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 12px;
    transition: var(--transition);
    backdrop-filter: blur(8px);
}
.doc-card:hover {
    background: rgba(30, 41, 59, 0.8);
    border-color: rgba(6, 182, 212, 0.4);
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
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
    position: relative;
    overflow: hidden;
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
    border-color: rgba(6, 182, 212, 0.4);
    color: var(--text-primary);
    transform: translateY(-2px);
}

/* ── Chat Messages ── */
.chat-message {
    padding: 1.25rem;
    margin-bottom: 1rem;
    border-radius: var(--radius-md);
    display: flex;
    gap: 1rem;
    transition: var(--transition);
}
.chat-message.user {
    background: rgba(30, 41, 59, 0.5);
    border: 1px solid rgba(255, 255, 255, 0.06);
}
.chat-message.assistant {
    background: rgba(17, 24, 39, 0.6);
    border: 1px solid rgba(6, 182, 212, 0.2);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.2);
}
.chat-avatar {
    width: 32px;
    height: 32px;
    border-radius: 8px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
}
.chat-avatar.user {
    background: #3B82F6;
    color: white;
}
.chat-avatar.assistant {
    background: linear-gradient(135deg, #06B6D4, #8B5CF6);
    color: white;
}
.chat-content {
    flex-grow: 1;
    font-family: var(--font-body);
    font-size: 0.95rem;
    line-height: 1.7;
    color: var(--text-primary);
}

/* ── Floating Chat Input ── */
.stChatInput {
    padding-bottom: 1.5rem !important;
}
.stChatInput textarea {
    background: rgba(17, 24, 39, 0.85) !important;
    backdrop-filter: blur(16px) !important;
    border: 1px solid rgba(255, 255, 255, 0.12) !important;
    border-radius: var(--radius-lg) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 0.95rem !important;
    padding: 0.85rem 1.25rem !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.5) !important;
    transition: var(--transition) !important;
}
.stChatInput textarea:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.25) !important;
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
    background: linear-gradient(135deg, #06B6D4, #3B82F6) !important;
    color: #FFFFFF !important;
    border: none !important;
}
.stButton > button[kind="primary"]:hover {
    box-shadow: 0 0 20px rgba(6, 182, 212, 0.4) !important;
}

/* ── Citations ── */
.citation {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 1.25rem;
    height: 1.25rem;
    padding: 0 5px;
    border-radius: 4px;
    background: rgba(6, 182, 212, 0.15);
    color: var(--accent-cyan);
    font-size: 0.72rem;
    font-weight: 700;
    font-family: var(--font-mono);
    vertical-align: super;
    margin: 0 2px;
    border: 1px solid rgba(6, 182, 212, 0.3);
    transition: var(--transition);
}
.citation:hover {
    background: var(--accent-cyan);
    color: #0A0D14;
}

</style>
"""

# ── Hero Welcome Screen (Midnight Luxe) ───────────────────────────────────────
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
