"""
frontend/styles.py
==================
Custom CSS for the PaperBrain Streamlit UI.
Academic Journal Aesthetic.
"""

CUSTOM_CSS = """
<style>
/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Lora:ital,wght@0,400;0,500;0,600;0,700;1,400&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── CSS Variables (Academic Journal) ── */
:root {
    --bg-primary:    #FDFDFB; /* Off-white paper */
    --bg-secondary:  #F4F4F0; /* Slightly darker paper for sidebar */
    --bg-card:       #FFFFFF;
    --bg-card-hover: #F8F8F6;
    --border:        #E2E1D9; /* Soft grey/sepia border */
    --border-dark:   #D5D4CB;
    --accent:        #8B7355; /* Muted Sepia/Gold */
    --accent-light:  #D2C9BB;
    --accent-dim:    rgba(139, 115, 85, 0.1);
    --success:       #556B2F; /* Dark Olive Green */
    --warning:       #D2B48C; /* Tan */
    --danger:        #8B0000; /* Dark Red */
    --text-primary:  #1A1A1A; /* Charcoal Black */
    --text-secondary:#4A4A4A; /* Soft grey */
    --text-muted:    #7A7A7A;
    --text-sidebar:  #2B2B2B; /* Dark text for light sidebar */
    
    --user-bubble:   #FFFFFF;
    --bot-bubble:    #F4F4F0;
    
    --font-ui:       'Inter', sans-serif;
    --font-reading:  'Lora', serif;
    --font-mono:     'JetBrains Mono', monospace;
    
    --radius-sm:     4px; /* Less rounded, more print-like */
    --radius-md:     6px;
    --radius-lg:     8px;
    --transition:    0.25s ease-out;
}

/* ── Base ── */
html, body, [class*="css"] {
    font-family: var(--font-reading) !important;
}

h1, h2, h3, h4, h5, h6 {
    font-family: var(--font-reading) !important;
    font-weight: 600 !important;
    color: var(--text-primary) !important;
    letter-spacing: -0.01em;
}

/* ── Main App Background ── */
.stApp {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

/* ── Hide Streamlit default Deploy button & footer ── */
.stDeployButton, 
[data-testid="stDeployButton"],
footer {
    display: none !important;
}
header[data-testid="stHeader"] {
    background-color: transparent !important;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
    box-shadow: none !important;
}
[data-testid="stSidebar"] .block-container {
    padding: 2rem 1.5rem !important;
}

/* Aggressively force text colors in sidebar to dark */
[data-testid="stSidebar"],
[data-testid="stSidebar"] * {
    color: var(--text-sidebar) !important;
    font-family: var(--font-ui) !important; /* Sidebar uses UI font */
}
[data-testid="stSidebar"] .stMarkdown p,
[data-testid="stSidebar"] .stMarkdown h1,
[data-testid="stSidebar"] .stMarkdown h2,
[data-testid="stSidebar"] .stMarkdown h3,
[data-testid="stSidebar"] .stMarkdown h4,
[data-testid="stSidebar"] .stText,
[data-testid="stSidebar"] label {
    color: var(--text-sidebar) !important;
}
[data-testid="stSidebar"] hr {
    border-top: 1px solid var(--border-dark) !important;
    margin: 1.5rem 0 !important;
}

/* Protect Material Symbols icons from font overrides */
[data-testid="stIconMaterial"], 
.material-symbols-rounded,
[class*="material-symbols"],
[data-testid="stSidebarCollapseButton"] * {
    font-family: 'Material Symbols Rounded', sans-serif !important;
}

/* ── Sidebar title ── */
.sidebar-title {
    font-family: var(--font-reading) !important;
    font-size: 1.4rem;
    font-weight: 700;
    color: var(--text-primary) !important;
    margin-bottom: 0.25rem;
    display: flex;
    align-items: center;
    gap: 8px;
    letter-spacing: -0.02em;
}
.sidebar-subtitle {
    font-family: var(--font-ui) !important;
    font-size: 0.75rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-muted) !important;
    margin-bottom: 1.5rem;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: transparent !important;
}
[data-testid="stFileUploadDropzone"] {
    background: var(--bg-card) !important; 
    border: 1px dashed var(--border-dark) !important;
    border-radius: var(--radius-sm) !important;
    padding: 1rem !important;
    transition: var(--transition) !important;
}
[data-testid="stFileUploadDropzone"]:hover {
    border-color: var(--accent) !important;
    background: var(--bg-card-hover) !important;
}
[data-testid="stFileUploadDropzone"] button {
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-ui) !important;
    font-size: 0.82rem !important;
    border: 1px solid var(--border-dark) !important;
    background: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}
[data-testid="stFileUploadDropzone"] button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
}

/* ── Document card ── */
.doc-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    padding: 1rem;
    border-radius: var(--radius-sm);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: flex-start;
    gap: 12px;
    transition: var(--transition);
}
.doc-card:hover {
    background: var(--bg-card-hover);
    border-color: var(--accent-light);
}
.doc-icon {
    font-size: 1.5rem;
    margin-top: 2px;
}
.doc-info {
    display: flex;
    flex-direction: column;
    gap: 4px;
}
.doc-name {
    font-family: var(--font-ui);
    font-weight: 600;
    font-size: 0.9rem;
    color: var(--text-primary);
    word-break: break-all;
}
.doc-meta {
    font-family: var(--font-ui);
    font-size: 0.75rem;
    color: var(--text-secondary);
}

/* ── Chat Messages ── */
.chat-message {
    padding: 1.5rem 0;
    margin-bottom: 0;
    display: flex;
    gap: 1.25rem;
    border-bottom: 1px solid var(--border);
}
.chat-message:last-child {
    border-bottom: none;
}
.chat-message.user {
    background-color: transparent;
}
.chat-message.assistant {
    background-color: transparent;
}
.chat-avatar {
    width: 32px;
    height: 32px;
    border-radius: 2px; /* Square blocky avatar */
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1rem;
    flex-shrink: 0;
    font-family: var(--font-ui);
}
.chat-avatar.user {
    background: var(--text-primary);
    color: white;
}
.chat-avatar.assistant {
    background: var(--accent);
    color: white;
}
.chat-content {
    flex-grow: 1;
    font-family: var(--font-reading);
    font-size: 1.05rem;
    line-height: 1.8;
    color: var(--text-primary);
}
.chat-content code {
    font-family: var(--font-mono) !important;
    font-size: 0.85em;
    background: var(--bg-secondary);
    padding: 0.2em 0.4em;
    border-radius: 2px;
    border: 1px solid var(--border);
    color: var(--text-primary);
}
.chat-content pre {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    padding: 1rem;
    border-radius: var(--radius-sm);
    overflow-x: auto;
}
.chat-content pre code {
    background: none;
    padding: 0;
    border: none;
}

/* ── Citations ── */
.citation {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 1.25rem;
    height: 1.25rem;
    padding: 0 4px;
    border-radius: 2px;
    background: var(--bg-secondary);
    color: var(--accent);
    font-size: 0.7rem;
    font-weight: 600;
    font-family: var(--font-ui);
    vertical-align: super;
    cursor: pointer;
    margin: 0 2px;
    border: 1px solid var(--border);
    transition: var(--transition);
}
.citation:hover {
    background: var(--accent);
    color: white;
    border-color: var(--accent);
}

/* ── Source Cards ── */
.source-panel {
    margin-top: 1.5rem;
    padding-top: 1.5rem;
    border-top: 1px solid var(--border);
}
.source-panel-title {
    font-family: var(--font-ui);
    font-size: 0.85rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
    margin-bottom: 1rem;
}
.source-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-left: 3px solid var(--accent);
    padding: 1rem;
    border-radius: var(--radius-sm);
    margin-bottom: 0.75rem;
}
.source-meta {
    font-family: var(--font-ui);
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.75rem;
    font-size: 0.75rem;
    color: var(--text-secondary);
    border-bottom: 1px solid var(--border);
    padding-bottom: 0.5rem;
}
.source-text {
    font-family: var(--font-reading);
    font-size: 0.95rem;
    line-height: 1.7;
    color: var(--text-secondary);
}

/* ── Metric badges ── */
.metric-badge {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 2px 6px;
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 2px;
    font-size: 0.7rem;
    font-weight: 500;
    font-family: var(--font-mono);
    color: var(--text-secondary);
}

/* ── Buttons (Streamlit Overrides) ── */
.stButton > button {
    border-radius: var(--radius-sm) !important;
    font-family: var(--font-ui) !important;
    font-weight: 500 !important;
    border: 1px solid var(--border-dark) !important;
    color: var(--text-primary) !important;
    background: var(--bg-card) !important;
    transition: var(--transition) !important;
}
.stButton > button:hover {
    border-color: var(--accent) !important;
    color: var(--accent) !important;
    background: var(--bg-card-hover) !important;
}
.stButton > button[kind="primary"] {
    background: var(--text-primary) !important;
    color: white !important;
    border-color: var(--text-primary) !important;
}
.stButton > button[kind="primary"]:hover {
    background: var(--accent) !important;
    border-color: var(--accent) !important;
}

/* ── Input Box (Chat Input) ── */
.stChatInput {
    padding-bottom: 2rem !important;
}
.stChatInput textarea {
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--border-dark) !important;
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    font-family: var(--font-reading) !important;
    font-size: 1.05rem !important;
}
.stChatInput textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 1px var(--accent) !important;
}
</style>
"""


# ── Welcome Panel (Academic Journal style) ────────────────────────────────────
WELCOME_PANEL_HTML = """
<div style="
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 4rem 2rem;
    text-align: center;
    max-width: 600px;
    margin: 0 auto;
">
    <div style="
        font-size: 3rem;
        margin-bottom: 1.5rem;
        opacity: 0.8;
    ">📖</div>
    <h2 style="
        font-family: 'Lora', serif;
        font-size: 1.8rem;
        font-weight: 600;
        color: #1A1A1A;
        margin-bottom: 0.75rem;
        letter-spacing: -0.02em;
    ">Ask <em>PaperBrain</em></h2>
    <p style="
        font-family: 'Lora', serif;
        font-size: 1rem;
        color: #4A4A4A;
        line-height: 1.8;
        margin-bottom: 0.25rem;
    ">Upload your PDFs and ask any question.</p>
    <p style="
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        color: #7A7A7A;
        margin-bottom: 2rem;
    ">Answers come <strong>only from your documents</strong> &mdash; zero hallucinations.</p>
    <div style="
        display: flex;
        gap: 1.5rem;
        flex-wrap: wrap;
        justify-content: center;
    ">
        <div style="
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            padding: 0.5rem 1rem;
            border: 1px solid #E2E1D9;
            border-radius: 4px;
            color: #4A4A4A;
            background: #F4F4F0;
        ">🔍 Semantic Search</div>
        <div style="
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            padding: 0.5rem 1rem;
            border: 1px solid #E2E1D9;
            border-radius: 4px;
            color: #4A4A4A;
            background: #F4F4F0;
        ">📑 Exact Citations</div>
        <div style="
            font-family: 'Inter', sans-serif;
            font-size: 0.8rem;
            padding: 0.5rem 1rem;
            border: 1px solid #E2E1D9;
            border-radius: 4px;
            color: #4A4A4A;
            background: #F4F4F0;
        ">🔒 100% Offline</div>
    </div>
</div>
"""


# ── Typing Indicator ──────────────────────────────────────────────────────────
TYPING_INDICATOR_HTML = """
<div style="
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 1rem 0;
">
    <div style="
        width: 32px;
        height: 32px;
        border-radius: 2px;
        background: #8B7355;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1rem;
    ">🧠</div>
    <div style="
        display: flex;
        gap: 4px;
        align-items: center;
    ">
        <div style="
            width: 6px; height: 6px;
            background: #8B7355;
            border-radius: 50%;
            animation: typingDot 1.4s ease-in-out infinite;
        "></div>
        <div style="
            width: 6px; height: 6px;
            background: #8B7355;
            border-radius: 50%;
            animation: typingDot 1.4s ease-in-out 0.2s infinite;
        "></div>
        <div style="
            width: 6px; height: 6px;
            background: #8B7355;
            border-radius: 50%;
            animation: typingDot 1.4s ease-in-out 0.4s infinite;
        "></div>
    </div>
</div>
<style>
@keyframes typingDot {
    0%, 60%, 100% { opacity: 0.3; transform: scale(0.8); }
    30% { opacity: 1; transform: scale(1.2); }
}
</style>
"""
