append_code = '''
def render_app_header(doc_count: int, llm_online: bool) -> None:
    status = '<span style="color:var(--success)">\\U0001f7e2 LLM Online</span>' if llm_online else '<span style="color:var(--danger)">\\U0001f534 LLM Offline</span>'
    st.markdown(f"""
        <div style="display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid var(--border);padding-bottom:0.75rem;margin-bottom:1.5rem">
            <h3 style="margin:0;font-weight:700;color:var(--text-primary);font-size:1.2rem">\\U0001f9e0 PaperBrain Chat</h3>
            <div style="font-size:0.8rem;color:var(--text-muted);font-weight:600">
                {doc_count} PDF{'s' if doc_count != 1 else ''} &middot; {status}
            </div>
        </div>
    """, unsafe_allow_html=True)
'''

with open('frontend/components.py', 'a', encoding='utf-8') as f:
    f.write(append_code)
print("Appended render_app_header")
