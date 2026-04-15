import streamlit as st
import requests

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GitHub Portfolio Reviewer",
    page_icon="🐙",
    layout="centered",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Global Reset ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* ── Background ── */
.stApp {
    background: #0d1117;
    color: #e6edf3;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }

/* ── Hero Section ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
}
.hero h1 {
    font-size: 2.8rem;
    font-weight: 700;
    background: linear-gradient(135deg, #58a6ff 0%, #bc8cff 50%, #ff7b72 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.5rem;
    line-height: 1.2;
}
.hero p {
    color: #8b949e;
    font-size: 1.05rem;
    margin-top: 0.5rem;
}

/* ── Input Box ── */
.stTextInput > div > div > input {
    background: #161b22 !important;
    border: 1px solid #30363d !important;
    color: #e6edf3 !important;
    border-radius: 10px !important;
    padding: 0.75rem 1rem !important;
    font-size: 1rem !important;
    transition: border-color 0.2s ease;
}
.stTextInput > div > div > input:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 3px rgba(88,166,255,0.15) !important;
}
.stTextInput label {
    color: #8b949e !important;
    font-size: 0.9rem !important;
    font-weight: 500 !important;
}

/* ── Button ── */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #238636, #2ea043) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.75rem 1.5rem !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.02em !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(46,160,67,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(46,160,67,0.45) !important;
}

/* ── Cards ── */
.card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    transition: border-color 0.2s ease;
}
.card:hover { border-color: #58a6ff55; }

.card-title {
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #58a6ff;
    margin-bottom: 0.75rem;
}

/* ── Stat Boxes ── */
.stats-grid {
    display: flex;
    gap: 1rem;
    margin: 1rem 0;
}
.stat-box {
    flex: 1;
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
}
.stat-number {
    font-size: 2rem;
    font-weight: 700;
    color: #58a6ff;
}
.stat-label {
    font-size: 0.78rem;
    color: #8b949e;
    margin-top: 0.2rem;
}

/* ── Repo Tags ── */
.repo-tag {
    display: inline-block;
    background: #21262d;
    border: 1px solid #30363d;
    color: #e6edf3;
    border-radius: 6px;
    padding: 0.3rem 0.7rem;
    font-size: 0.82rem;
    margin: 0.25rem;
    font-family: 'Courier New', monospace;
}
.repo-tag::before { content: "📁 "; }

/* ── Language Pills ── */
.lang-pill {
    display: inline-block;
    border-radius: 20px;
    padding: 0.25rem 0.9rem;
    font-size: 0.8rem;
    font-weight: 600;
    margin: 0.25rem;
    color: #fff;
}

/* ── Feedback Section ── */
.feedback-box {
    background: #161b22;
    border: 1px solid #30363d;
    border-left: 3px solid #bc8cff;
    border-radius: 12px;
    padding: 1.5rem;
    margin: 1rem 0;
    color: #c9d1d9;
    font-size: 0.97rem;
    line-height: 1.75;
    white-space: pre-wrap;
}

/* ── Divider ── */
.divider {
    border: none;
    border-top: 1px solid #21262d;
    margin: 1.5rem 0;
}

/* ── Success Banner ── */
.success-banner {
    background: linear-gradient(135deg, #0d2818, #1a3a2a);
    border: 1px solid #2ea043;
    border-radius: 10px;
    padding: 0.8rem 1.2rem;
    color: #3fb950;
    font-weight: 600;
    font-size: 0.95rem;
    margin: 1rem 0;
    text-align: center;
}

/* ── Error Banner ── */
.error-banner {
    background: #2d1117;
    border: 1px solid #f85149;
    border-radius: 10px;
    padding: 0.8rem 1.2rem;
    color: #ff7b72;
    font-weight: 500;
    font-size: 0.95rem;
    margin: 1rem 0;
    text-align: center;
}

/* ── Spinner ── */
.stSpinner > div { border-top-color: #58a6ff !important; }
</style>
""", unsafe_allow_html=True)

# ─── Language Color Map ──────────────────────────────────────────────────────
LANG_COLORS = {
    "Python":     "#3572A5",
    "JavaScript": "#f1e05a",
    "TypeScript": "#2b7489",
    "Java":       "#b07219",
    "C":          "#555555",
    "C++":        "#f34b7d",
    "Go":         "#00ADD8",
    "Rust":       "#dea584",
    "HTML":       "#e34c26",
    "CSS":        "#563d7c",
    "Ruby":       "#701516",
    "PHP":        "#4F5D95",
    "Swift":      "#F05138",
    "Kotlin":     "#7F52FF",
    "Shell":      "#89e051",
    "Dart":       "#00B4AB",
    "R":          "#276DC3",
}

def lang_pill(lang):
    color = LANG_COLORS.get(lang, "#8b949e")
    return f'<span class="lang-pill" style="background:{color};">{lang}</span>'

# ─── Hero ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <h1>🐙 GitHub Portfolio Reviewer</h1>
    <p>AI-powered code mentor feedback for student portfolios</p>
</div>
""", unsafe_allow_html=True)

# ─── Input Section ───────────────────────────────────────────────────────────
username = st.text_input("GitHub Username", placeholder="e.g. torvalds")

analyze_clicked = st.button("🔍 Analyze Portfolio")

# ─── Logic ───────────────────────────────────────────────────────────────────
if analyze_clicked:
    if not username.strip():
        st.markdown('<div class="error-banner">⚠️ Please enter a GitHub username.</div>', unsafe_allow_html=True)
    else:
        with st.spinner(f"Analyzing **{username}**'s repositories…"):
            try:
                response = requests.post(
                    f"https://github-reviewer-api-rh26.onrender.com/review?username={username.strip()}",
                    timeout=60
                )

                if response.status_code == 200:
                    data = response.json()
                    github_data = data.get("extracted_data", {})
                    feedback    = data.get("mentor_feedback", "")

                    # ── Success Banner ──
                    st.markdown(f'<div class="success-banner">✅ Analysis complete for <strong>{data.get("username", username)}</strong></div>', unsafe_allow_html=True)

                    # ── Stats Row ──
                    repo_count = github_data.get("public_repos_count", 0)
                    lang_count = len(github_data.get("primary_languages", []))
                    repo_list  = github_data.get("recent_repos", [])

                    st.markdown(f"""
                    <div class="stats-grid">
                        <div class="stat-box">
                            <div class="stat-number">{repo_count}</div>
                            <div class="stat-label">Public Repos</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-number">{len(repo_list)}</div>
                            <div class="stat-label">Recent Repos</div>
                        </div>
                        <div class="stat-box">
                            <div class="stat-number">{lang_count}</div>
                            <div class="stat-label">Languages Used</div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    # ── Recent Repos Card ──
                    if repo_list:
                        repo_tags = "".join([f'<span class="repo-tag">{r}</span>' for r in repo_list])
                        st.markdown(f"""
                        <div class="card">
                            <div class="card-title">📂 Recent Repositories</div>
                            {repo_tags}
                        </div>
                        """, unsafe_allow_html=True)

                    # ── Languages Card ──
                    langs = github_data.get("primary_languages", [])
                    if langs:
                        pills = "".join([lang_pill(l) for l in langs])
                        st.markdown(f"""
                        <div class="card">
                            <div class="card-title">💻 Primary Languages</div>
                            {pills}
                        </div>
                        """, unsafe_allow_html=True)

                    # ── AI Feedback Card ──
                    if feedback:
                        st.markdown(f"""
                        <div class="card">
                            <div class="card-title">🤖 AI Mentor Feedback</div>
                            <div class="feedback-box">{feedback}</div>
                        </div>
                        """, unsafe_allow_html=True)

                else:
                    st.markdown(f'<div class="error-banner">❌ Backend error: HTTP {response.status_code}</div>', unsafe_allow_html=True)

            except requests.exceptions.Timeout:
                st.markdown('<div class="error-banner">⏳ Request timed out. The backend might be cold-starting on Render — please try again in 30 seconds.</div>', unsafe_allow_html=True)
            except Exception as e:
                st.markdown(f'<div class="error-banner">🔌 Could not connect to the backend.<br><small>{str(e)}</small></div>', unsafe_allow_html=True)

# ─── Footer ──────────────────────────────────────────────────────────────────
st.markdown("""
<hr class="divider">
<p style="text-align:center; color:#484f58; font-size:0.8rem;">
    Powered by LangGraph · Groq Llama 3.1 · GitHub API
</p>
""", unsafe_allow_html=True)