import streamlit as st

st.set_page_config(page_title="YouTube RAG", layout="wide")

st.markdown(
    """
<style>
html, body, [class*="css"] {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
}

#MainMenu {visibility: hidden;}
header {visibility: hidden;}
footer {visibility: hidden;}

body {
    background: radial-gradient(circle at top, #1a1f3b 0, #050610 45%, #050610 100%);
}

.app-shell {
    max-width: 900px;
    margin: 0 auto;
    padding: 32px 16px 24px 16px;
    color: #f8f8ff;
}

.app-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
}

.app-title-left {
    display: flex;
    align-items: center;
    gap: 10px;
}

.logo-pill {
    width: 34px;
    height: 34px;
    border-radius: 999px;
    background: radial-gradient(circle at 30% 0, #ff4b9f, #5b5bff 50%, #18181f 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 18px rgba(91, 91, 255, 0.5);
    font-size: 18px;
}

.app-title {
    font-size: 22px;
    font-weight: 600;
    letter-spacing: 0.02em;
}

.app-subtitle {
    font-size: 14px;
    color: #a5a7c7;
    margin-top: 3px;
}

.status-pill {
    padding: 6px 12px;
    border-radius: 999px;
    font-size: 12px;
    background: rgba(35, 194, 123, 0.12);
    color: #46d39a;
    border: 1px solid rgba(70, 211, 154, 0.35);
}

.card {
    border-radius: 20px;
    padding: 16px 18px;
    background: linear-gradient(135deg, rgba(31, 33, 57, 0.92), rgba(8, 9, 22, 0.96));
    border: 1px solid rgba(111, 118, 255, 0.28);
    box-shadow: 0 28px 60px rgba(0, 0, 0, 0.75);
    margin-bottom: 18px;
}

.card-label {
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 0.12em;
    color: #8c8ea8;
    margin-bottom: 10px;
}

.video-input-container input {
    border-radius: 14px !important;
    padding: 12px 14px !important;
    font-size: 14px !important;
    background-color: rgba(9, 10, 26, 0.85) !important;
    border: 1px solid rgba(121, 129, 255, 0.5) !important;
    color: #f5f5ff !important;
}

.video-helper {
    font-size: 12px;
    color: #7d7fa8;
    margin-top: 7px;
}

.chat-wrapper {
    margin-top: 10px;
    height: calc(100vh - 260px);
    max-height: 620px;
    border-radius: 22px;
    background: radial-gradient(circle at top left, rgba(67, 97, 238, 0.18), transparent 56%),
                radial-gradient(circle at top right, rgba(244, 114, 182, 0.14), transparent 58%),
                rgba(8, 9, 22, 0.96);
    border: 1px solid rgba(80, 84, 140, 0.8);
    box-shadow: 0 22px 55px rgba(0, 0, 0, 0.8);
    padding: 16px 16px 80px 16px;
    position: relative;
    overflow: hidden;
}

.chat-scroll {
    height: 100%;
    overflow-y: auto;
    padding-right: 6px;
}

.message-row {
    display: flex;
    margin-bottom: 14px;
}

.message-user-bubble {
    margin-left: auto;
    max-width: 76%;
    background: linear-gradient(135deg, #2f6bff, #9b6bff);
    border-radius: 18px;
    padding: 11px 14px;
    font-size: 14.5px;
    line-height: 1.5;
    color: #fdfdff;
    box-shadow: 0 14px 30px rgba(26, 115, 232, 0.6);
}

.message-assistant-bubble {
    margin-right: auto;
    max-width: 78%;
    background: rgba(11, 12, 30, 0.98);
    border-radius: 18px;
    padding: 11px 14px;
    font-size: 14.5px;
    line-height: 1.55;
    color: #f6f7ff;
    border: 1px solid rgba(103, 110, 255, 0.6);
    box-shadow: 0 14px 30px rgba(0, 0, 0, 0.85);
}

.message-meta {
    font-size: 11px;
    color: #72759c;
    margin-top: 4px;
}

.empty-state {
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    color: #8f92bd;
    text-align: center;
    gap: 8px;
}

.empty-pill {
    padding: 5px 12px;
    border-radius: 999px;
    font-size: 11px;
    background: rgba(20, 22, 50, 0.95);
    border: 1px solid rgba(110, 119, 255, 0.7);
    color: #c3c5ff;
}

.empty-title {
    font-size: 15px;
}

.empty-sub {
    font-size: 13px;
    max-width: 270px;
}

.input-bar-container {
    position: fixed;
    left: 0;
    right: 0;
    bottom: 10px;
    display: flex;
    justify-content: center;
    pointer-events: none;
}

.input-bar-inner {
    pointer-events: auto;
    max-width: 900px;
    width: 100%;
    padding: 0 16px;
}

.stChatInputContainer textarea {
    border-radius: 999px !important;
    padding: 14px 18px !important;
    font-size: 15px !important;
    border: 1px solid rgba(102, 112, 255, 0.7) !important;
    background-color: rgba(9, 10, 26, 0.96) !important;
    color: #f8f9ff !important;
}

.stChatInputContainer div[data-baseweb="button"] {
    border-radius: 999px !important;
    background: linear-gradient(135deg, #306bff, #aa5bff) !important;
    border: none !important;
}

</style>
""",
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "video_id" not in st.session_state:
    st.session_state.video_id = ""

st.markdown("<div class='app-shell'>", unsafe_allow_html=True)

col1, col2 = st.columns([4, 1.6])
with col1:
    st.markdown(
        """
        <div class="app-header">
            <div class="app-title-left">
                <div class="logo-pill">▶</div>
                <div>
                    <div class="app-title">YouTube RAG Studio</div>
                    <div class="app-subtitle">Ask deep questions on any video in real time.</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    status_label = (
        "<div class='status-pill'>Video not loaded</div>"
        if not st.session_state.video_id
        else "<div class='status-pill'>Video linked • Ready</div>"
    )
    st.markdown(status_label, unsafe_allow_html=True)

with st.container():
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<div class="card-label">Video</div>', unsafe_allow_html=True)
    with st.container():
        st.markdown('<div class="video-input-container">', unsafe_allow_html=True)
        video_input = st.text_input(
            "",
            placeholder="Paste a YouTube URL or video ID to ground the chat...",
            value=st.session_state.video_id,
            key="video_input",
            label_visibility="collapsed",
        )
        st.markdown(
            "<div class='video-helper'>Your questions will be answered using this video's transcript.</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

if video_input != st.session_state.video_id:
    st.session_state.video_id = video_input.strip()
    st.session_state.messages = []

st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="chat-scroll">', unsafe_allow_html=True)

if len(st.session_state.messages) == 0:
    st.markdown(
        """
        <div class="empty-state">
            <div class="empty-pill">Ready when you are</div>
            <div class="empty-title">Start a conversation</div>
            <div class="empty-sub">Ask about key ideas, timestamps, explanations, or summaries from the video.</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
else:
    for role, msg in st.session_state.messages:
        if role == "user":
            st.markdown(
                f"""
                <div class="message-row">
                  <div class="message-user-bubble">{msg}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                f"""
                <div class="message-row">
                  <div class="message-assistant-bubble">{msg}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="input-bar-container"><div class="input-bar-inner">', unsafe_allow_html=True)
user_query = st.chat_input("Ask anything about the linked YouTube video...")
st.markdown("</div></div>", unsafe_allow_html=True)

if user_query:
    st.session_state.messages.append(("user", user_query))
    placeholder_answer = "Thinking based on the video context... (connect backend here)"
    st.session_state.messages.append(("assistant", placeholder_answer))
    st.experimental_rerun()

st.markdown("</div>", unsafe_allow_html=True)
