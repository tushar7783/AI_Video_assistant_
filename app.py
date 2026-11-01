"""Streamlit front-end for the AI Video Assistant — 'Midnight Emerald' theme.

Run with:  streamlit run app.py
Repo:      https://github.com/tushar7783/AI_Video_assistant_
"""
import streamlit as st
import time
import logging
from dotenv import load_dotenv
from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarizer import summarize, generate_title
from core.extractor import extract_action_items, extract_key_decisions, extract_questions
from core.Rag_engine import build_rag_chain, ask_question

load_dotenv()
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

LANGUAGES = ["english", "hinglish"]
STEPS = {
    "audio": "Audio processing",
    "transcript": "Transcription",
    "title": "Title generation",
    "summary": "Summarisation",
    "extract": "Action items, decisions & questions",
    "rag": "Building chat index",
}

st.set_page_config(
    page_title="AI Video Assistant",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── Theme: midnight navy, emerald primary, gold accent, glass cards ────────────
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&display=swap');

:root {
    --bg: #0a1224;
    --bg-2: #0f1a33;
    --card: rgba(255,255,255,.045);
    --card-solid: #121d38;
    --line: rgba(255,255,255,.09);
    --ink: #e9eefb;
    --muted: #8b99b8;
    --emerald: #34d399;
    --emerald-dark: #059669;
    --gold: #fbbf24;
    --rose: #fb7185;
}

html, body, .stApp, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp {
    background:
        radial-gradient(900px 500px at 85% -10%, rgba(52,211,153,.14), transparent 60%),
        radial-gradient(700px 400px at -5% 10%, rgba(251,191,36,.08), transparent 55%),
        var(--bg) !important;
    color: var(--ink) !important;
}
.stApp p, .stApp li, .stApp label, .stApp span, .stApp div[data-testid="stMarkdownContainer"] { color: var(--ink); }
header[data-testid="stHeader"] { background: transparent; }
section[data-testid="stSidebar"], div[data-testid="collapsedControl"], div[data-testid="stSidebarCollapsedControl"] { display: none; }
.block-container { padding-top: 2.2rem; max-width: 1280px; }

h1, h2, h3, h4 { font-family: 'Space Grotesk', sans-serif !important; color: var(--ink) !important; letter-spacing: -0.015em; }
h3 { font-size: 1.05rem !important; margin: 0 0 .5rem !important; }

/* ── Hero ── */
.hero { text-align: center; padding: 1.2rem 0 1.6rem; }
.hero .eyebrow {
    display: inline-block; padding: .3rem .9rem; border-radius: 999px; font-size: .72rem; font-weight: 600;
    letter-spacing: .16em; text-transform: uppercase; color: var(--emerald) !important;
    background: rgba(52,211,153,.1); border: 1px solid rgba(52,211,153,.3);
}
.hero h1 {
    font-size: clamp(2.2rem, 5vw, 3.6rem); font-weight: 700; margin: .9rem 0 .4rem; line-height: 1.05;
    background: linear-gradient(100deg, #ffffff 10%, var(--emerald) 55%, var(--gold) 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;
}
.hero p { color: var(--muted) !important; font-size: 1rem; margin: 0; }

/* ── Input bar (form) ── */
div[data-testid="stForm"] {
    background: var(--card); border: 1px solid var(--line); border-radius: 18px; padding: .9rem 1rem .4rem;
    backdrop-filter: blur(10px); box-shadow: 0 20px 50px rgba(0,0,0,.35);
}
.stTextInput input, div[data-baseweb="select"] > div {
    background: rgba(255,255,255,.05) !important; border: 1px solid var(--line) !important;
    border-radius: 12px !important; color: var(--ink) !important; min-height: 46px;
}
.stTextInput input::placeholder { color: #6b7a99 !important; }
.stTextInput input:focus { border-color: var(--emerald) !important; box-shadow: 0 0 0 3px rgba(52,211,153,.18) !important; }
div[data-baseweb="select"] span, div[data-baseweb="select"] svg { color: var(--ink) !important; fill: var(--ink) !important; }
div[data-baseweb="popover"] ul { background: var(--card-solid) !important; }
div[data-baseweb="popover"] li { color: var(--ink) !important; }

/* ── Buttons ── */
.stButton > button, .stFormSubmitButton > button, .stDownloadButton > button {
    border-radius: 12px; font-weight: 600; min-height: 46px; transition: all .15s ease;
    background: rgba(255,255,255,.06); color: var(--ink); border: 1px solid var(--line);
}
.stButton > button:hover, .stDownloadButton > button:hover { border-color: var(--emerald); color: var(--emerald); }
.stFormSubmitButton > button[kind="primaryFormSubmit"] {
    background: linear-gradient(135deg, var(--emerald), var(--emerald-dark)); color: #04231a !important; border: none; font-weight: 700;
    box-shadow: 0 8px 22px rgba(52,211,153,.35);
}
.stFormSubmitButton > button[kind="primaryFormSubmit"]:hover { transform: translateY(-1px); box-shadow: 0 12px 28px rgba(52,211,153,.5); color: #04231a !important; }

/* ── Title row ── */
.session-title { font-family: 'Space Grotesk', sans-serif; font-size: 1.7rem; font-weight: 700; margin: 0; }
.session-kicker { font-size: .7rem; letter-spacing: .16em; text-transform: uppercase; color: var(--gold) !important; font-weight: 600; }

/* ── Metrics ── */
div[data-testid="stMetric"] {
    background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: .9rem 1.1rem;
    border-left: 3px solid var(--emerald);
}
div[data-testid="stMetricLabel"] p { color: var(--muted) !important; font-size: .7rem; text-transform: uppercase; letter-spacing: .12em; }
div[data-testid="stMetricValue"] { font-family: 'Space Grotesk', sans-serif; color: var(--ink) !important; font-size: 1.6rem; }

/* ── Glass cards ── */
[class*="st-key-card"], [class*="st-key-chat_panel"] {
    background: var(--card); border: 1px solid var(--line); border-radius: 18px; padding: 1.2rem 1.4rem;
    backdrop-filter: blur(8px); box-shadow: 0 10px 30px rgba(0,0,0,.25);
}
.st-key-card_summary { border-top: 3px solid var(--emerald); }
.st-key-card_insights { border-top: 3px solid var(--gold); }
.st-key-chat_panel   { border-top: 3px solid var(--rose); }

/* ── Tabs ── */
div[data-baseweb="tab-list"] { gap: .4rem; border-bottom: 1px solid var(--line); }
button[data-baseweb="tab"] { font-weight: 600; color: var(--muted); background: transparent; }
button[data-baseweb="tab"][aria-selected="true"] { color: var(--gold) !important; }
div[data-baseweb="tab-highlight"] { background-color: var(--gold) !important; }

/* ── Chat ── */
div[data-testid="stChatMessage"] { background: rgba(255,255,255,.04); border: 1px solid var(--line); border-radius: 14px; padding: .8rem 1rem; }
div[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) { background: rgba(52,211,153,.1); border-color: rgba(52,211,153,.3); }
div[data-testid="stChatInput"] { border-radius: 14px; }
div[data-testid="stChatInput"] textarea { color: var(--ink) !important; }
div[data-testid="stBottomBlockContainer"], div[data-testid="stChatInput"] > div { background: transparent !important; }

/* ── Misc ── */
div[data-testid="stStatus"], div[data-testid="stExpander"] {
    background: var(--card); border: 1px solid var(--line); border-radius: 14px;
}
.stTextArea textarea { background: rgba(255,255,255,.04) !important; color: var(--muted) !important; border: 1px solid var(--line) !important; border-radius: 12px !important; }
hr { border-color: var(--line) !important; }
.stCaption, small { color: var(--muted) !important; }
.empty { text-align: center; padding: 3rem 1rem 1rem; }
.empty .row { display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; margin-top: 1.2rem; }
.empty .tile {
    background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 1.1rem 1.4rem; min-width: 200px;
}
.empty .tile b { display: block; font-family: 'Space Grotesk', sans-serif; margin: .3rem 0 .15rem; }
.empty .tile span { color: var(--muted) !important; font-size: .82rem; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-thumb { background: rgba(255,255,255,.15); border-radius: 3px; }
</style>
""",
    unsafe_allow_html=True,
)

# ─── Session state ──────────────────────────────────────────────────────────────
for key, default in {
    "result": None,
    "chat_history": [],
    "language": "english",
}.items():
    st.session_state.setdefault(key, default)


# ─── Helpers ────────────────────────────────────────────────────────────────────
def word_count(text: str) -> int:
    return len(text.split())


def build_report(r: dict) -> str:
    """Markdown report of the analysis (used for the download button)."""
    return (
        f"# {r['title']}\n\n"
        f"## Summary\n{r['summary']}\n\n"
        f"## Action Items\n{r['action_items']}\n\n"
        f"## Key Decisions\n{r['key_decisions']}\n\n"
        f"## Open Questions\n{r['open_questions']}\n\n"
        f"## Transcript\n{r['transcript']}\n"
    )


def run_pipeline(source: str, language: str, on_step) -> dict:
    """Run every stage in order, reporting progress via on_step(key, state)."""
    started = time.perf_counter()

    on_step("audio", "active")
    chunks = process_input(source)
    on_step("audio", "done")

    on_step("transcript", "active")
    transcript = transcribe_all(chunks, language)
    if not transcript or not transcript.strip():
        raise ValueError("Transcription returned no text.")
    on_step("transcript", "done")

    on_step("title", "active")
    title = generate_title(transcript)
    on_step("title", "done")

    on_step("summary", "active")
    summary = summarize(transcript)
    on_step("summary", "done")

    on_step("extract", "active")
    action_items = extract_action_items(transcript)
    decisions = extract_key_decisions(transcript)
    questions = extract_questions(transcript)
    on_step("extract", "done")

    on_step("rag", "active")
    rag_chain = build_rag_chain(transcript)
    on_step("rag", "done")

    return {
        "title": title,
        "transcript": transcript,
        "summary": summary,
        "action_items": action_items,
        "key_decisions": decisions,
        "open_questions": questions,
        "rag_chain": rag_chain,
        "elapsed": time.perf_counter() - started,
    }


def analyse(source: str, language: str) -> None:
    """Run the pipeline inside a live status panel and store the result."""
    if not source.strip():
        st.error("Please enter a YouTube URL or file path.")
        return

    st.session_state.result = None
    st.session_state.chat_history = []

    with st.status("Analysing your video…", expanded=True) as status:
        current = {"step": None}

        def on_step(key: str, state: str) -> None:
            current["step"] = key
            icon = "⏳" if state == "active" else "✅"
            st.write(f"{icon} {STEPS[key]}{'…' if state == 'active' else ''}")

        try:
            st.session_state.result = run_pipeline(source.strip(), language, on_step)
        except Exception as exc:  # noqa: BLE001 - surface any failure in the UI
            logger.exception("Pipeline failed at step %s", current["step"])
            failed = STEPS.get(current["step"], "Pipeline")
            status.update(label=f"{failed} failed", state="error")
            st.error(f"{failed} failed: {exc}")
            return

        status.update(label="Analysis complete", state="complete", expanded=False)


# ─── Section renderers ──────────────────────────────────────────────────────────
def render_insights(r: dict) -> None:
    with st.container(key="card_insights"):
        tab_a, tab_d, tab_q = st.tabs(["✅ Action Items", "🔑 Key Decisions", "❓ Open Questions"])
        with tab_a:
            st.markdown(r["action_items"])
        with tab_d:
            st.markdown(r["key_decisions"])
        with tab_q:
            st.markdown(r["open_questions"])


def render_chat(r: dict) -> None:
    with st.container(key="chat_panel"):
        head, clear = st.columns([4, 1])
        head.subheader("💬 Chat with your video")
        if clear.button("Clear", key="clear_chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()

        messages = st.container(height=430, border=False)
        prompt = st.chat_input("Ask about this video…")

        # Handle the new question first so it shows up in the same run
        if prompt:
            st.session_state.chat_history.append({"role": "user", "content": prompt})
            with st.spinner("Thinking…"):
                try:
                    answer = ask_question(r["rag_chain"], prompt)
                except Exception:  # noqa: BLE001
                    logger.exception("RAG query failed")
                    answer = "Sorry, I couldn't answer that. Is Ollama running?"
            st.session_state.chat_history.append({"role": "assistant", "content": answer})

        with messages:
            if not st.session_state.chat_history:
                st.caption("Try: “What are the key takeaways?” or “What did the speaker say about …?”")
            for msg in st.session_state.chat_history:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])


# ─── Hero + input bar ───────────────────────────────────────────────────────────
st.markdown(
    """
<div class="hero">
    <span class="eyebrow">Meeting Intelligence</span>
    <h1>AI Video Assistant</h1>
    <p>Transcribe, summarise and chat with any video or recording.</p>
</div>
""",
    unsafe_allow_html=True,
)

with st.form("input_form", border=True):
    c_src, c_lang, c_btn = st.columns([5, 1.4, 1.4], vertical_alignment="bottom")
    source = c_src.text_input("YouTube URL or file path", placeholder="Paste a YouTube link or a local file path…")
    language = c_lang.selectbox("Language", LANGUAGES, format_func=str.title)
    submitted = c_btn.form_submit_button("⚡ Analyse", type="primary", use_container_width=True)

if submitted:
    st.session_state.language = language
    analyse(source, language)

# ─── Results ────────────────────────────────────────────────────────────────────
result = st.session_state.result

if result:
    st.write("")
    t_col, d_col = st.columns([5, 1.3], vertical_alignment="center")
    with t_col:
        st.markdown('<div class="session-kicker">Session</div>', unsafe_allow_html=True)
        st.header(result["title"])
    with d_col:
        st.download_button(
            "⬇️ Report (.md)",
            data=build_report(result),
            file_name="meeting_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

    m1, m2, m3 = st.columns(3)
    m1.metric("Transcript words", f"{word_count(result['transcript']):,}")
    m2.metric("Processing time", f"{result['elapsed']:.0f}s")
    m3.metric("Language", st.session_state.language.title())

    st.write("")
    left, right = st.columns([3, 2], gap="large")
    with left:
        with st.container(key="card_summary"):
            st.subheader("📋 Summary")
            st.markdown(result["summary"])
        st.write("")
        render_insights(result)
    with right:
        render_chat(result)

    st.write("")
    with st.expander("📝 Full transcript"):
        st.text_area("Transcript", result["transcript"], height=380, label_visibility="collapsed")

elif not submitted:
    st.markdown(
        """
<div class="empty">
    <div class="row">
        <div class="tile">🎙️<b>Transcribe</b><span>Whisper turns speech into text</span></div>
        <div class="tile">📋<b>Summarise</b><span>Summary, actions &amp; decisions</span></div>
        <div class="tile">💬<b>Chat</b><span>Ask questions, get grounded answers</span></div>
    </div>
</div>
""",
        unsafe_allow_html=True,
    )