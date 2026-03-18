import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI 책쓰기의 신",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="collapsed"
)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "result" not in st.session_state:
    st.session_state.result = ""

st.markdown("""
<style>
/* ===== 기본 ===== */
html, body, [class*="css"] {
    font-family: "Pretendard", "Noto Sans KR", sans-serif;
}

html, body, .stApp {
    background: linear-gradient(180deg, #040814 0%, #020611 100%);
    overflow: hidden;
}

/* ===== 스트림릿 기본 요소 숨기기 ===== */
header, footer {
    visibility: hidden !important;
    height: 0 !important;
}

#MainMenu,
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    display: none !important;
}

/* ===== 상단 여백 제거 ===== */
.block-container {
    max-width: 100vw !important;
    padding-top: 0 !important;
    padding-bottom: 0 !important;
    padding-left: 0 !important;
    padding-right: 0 !important;
    margin-top: 0 !important;
}

section.main > div {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

div[data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

[data-testid="stHorizontalBlock"] {
    gap: 0 !important;
}

/* ===== 좌측 패널 ===== */
.left-wrap {
    min-height: 100vh;
    background: linear-gradient(180deg, rgba(47,48,61,0.98) 0%, rgba(34,36,49,0.98) 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
    padding: 26px 26px 40px 26px;
    box-sizing: border-box;
}

.left-top {
    display: flex;
    justify-content: flex-end;
    color: rgba(255,255,255,0.9);
    font-size: 30px;
    line-height: 1;
    margin-bottom: 44px;
}

.left-title {
    color: #ffffff;
    font-size: 25px;
    font-weight: 800;
    line-height: 1.45;
    word-break: keep-all;
    margin-bottom: 30px;
}

.left-sub {
    color: #ffffff;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 20px;
}

.left-list {
    color: #ffffff;
    font-size: 17px;
    font-weight: 700;
    line-height: 1.7;
    padding-left: 28px;
}

.left-list li {
    margin-bottom: 12px;
}

/* ===== 우측 메인 ===== */
.right-wrap {
    min-height: 100vh;
    position: relative;
    background:
        radial-gradient(circle at 50% 22%, rgba(45, 73, 140, 0.18) 0%, rgba(5,9,20,0) 18%),
        linear-gradient(180deg, #020714 0%, #030814 100%);
    overflow: hidden;
}

.right-menu {
    position: absolute;
    top: 12px;
    right: 20px;
    color: rgba(255,255,255,0.88);
    font-size: 28px;
    z-index: 5;
}

.hero-shell {
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 30px 140px 30px;
    text-align: center;
    box-sizing: border-box;
}

.hero-icon-box {
    width: 250px;
    height: 250px;
    border-radius: 24px;
    margin-bottom: 26px;
    background:
        repeating-linear-gradient(
            135deg,
            rgba(255,255,255,0.018) 0px,
            rgba(255,255,255,0.018) 2px,
            transparent 2px,
            transparent 10px
        );
    display: flex;
    align-items: center;
    justify-content: center;
}

.hero-icon {
    font-size: 120px;
    filter: grayscale(1) brightness(0.72);
}

.hero-title {
    color: #ffffff;
    font-size: 60px;
    font-weight: 900;
    line-height: 1.18;
    letter-spacing: -0.03em;
    margin-bottom: 14px;
    word-break: keep-all;
}

.hero-author {
    color: #c6cede;
    font-size: 16px;
}

.hero-author strong {
    color: #ffffff;
}

/* ===== 입력창 ===== */
.input-fixed {
    position: fixed;
    left: calc(28% + ((72% - 28%) / 2));
    transform: translateX(-50%);
    bottom: 28px;
    width: min(820px, calc(100vw - 470px));
    z-index: 30;
}

.input-shell {
    position: relative;
    width: 100%;
}

div[data-testid="stTextInput"] {
    margin: 0 !important;
}

div[data-testid="stTextInput"] > div {
    background: transparent !important;
}

div[data-testid="stTextInput"] input {
    height: 64px !important;
    min-height: 64px !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    background: rgba(49, 53, 69, 0.82) !important;
    color: #ffffff !important;
    font-size: 18px !important;
    padding-left: 18px !important;
    padding-right: 74px !important;
    box-shadow: none !important;
}

div[data-testid="stTextInput"] input::placeholder {
    color: #8d93a6 !important;
    opacity: 1 !important;
}

.send-btn-wrap {
    position: absolute;
    right: 10px;
    top: 12px;
    z-index: 50;
}

.stButton > button {
    width: 46px !important;
    min-width: 46px !important;
    height: 40px !important;
    min-height: 40px !important;
    border-radius: 10px !important;
    border: none !important;
    background: rgba(255,255,255,0.08) !important;
    color: #d6dae5 !important;
    font-size: 20px !important;
    font-weight: 800 !important;
    padding: 0 !important;
    box-shadow: none !important;
}

.stButton > button:hover {
    background: rgba(255,255,255,0.14) !important;
    color: #ffffff !important;
}

/* ===== 결과창 ===== */
.result-shell {
    position: fixed;
    left: 30%;
    right: 28px;
    bottom: 108px;
    max-height: 42vh;
    overflow: auto;
    background: rgba(12, 17, 30, 0.92);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 22px 24px;
    box-sizing: border-box;
    backdrop-filter: blur(10px);
    z-index: 25;
}

.result-title {
    color: #ffffff;
    font-size: 18px;
    font-weight: 800;
    margin-bottom: 12px;
}

.result-box {
    color: #d9dfed;
    font-size: 15px;
    line-height: 1.85;
    white-space: pre-wrap;
    word-break: keep-all;
}

.download-wrap {
    margin-top: 16px;
}

div[data-testid="stDownloadButton"] > button {
    width: 100% !important;
    height: 48px !important;
    min-height: 48px !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    background: rgba(255,255,255,0.05) !important;
    color: white !important;
    font-weight: 700 !important;
}

/* ===== 모바일 ===== */
@media (max-width: 1100px) {
    .left-wrap {
        display: none;
    }

    .hero-title {
        font-size: 42px;
    }

    .hero-icon-box {
        width: 200px;
        height: 200px;
    }

    .hero-icon {
        font-size: 96px;
    }

    .input-fixed {
        left: 50%;
        width: calc(100vw - 40px);
    }

    .result-shell {
        left: 20px;
        right: 20px;
        bottom: 100px;
    }
}
</style>
""", unsafe_allow_html=True)

left, right = st.columns([1.05, 2.35], gap="small")

with left:
    st.markdown('<div class="left-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="left-top">×</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="left-title">
            하루에 책 한권을 쓰는 챗쓰기의 신 등장, 그 이름은 바로 AI 책쓰기의 신!
        </div>
    """, unsafe_allow_html=True)
    st.markdown('<div class="left-sub">• 사용 예시 :</div>', unsafe_allow_html=True)
    st.markdown("""
        <ol class="left-list">
            <li>"효율적으로 글을 쓰는 방법은?"</li>
            <li>"책으로 독자들에게 감동을 주는 방법은?"</li>
            <li>"어떻게 하루 1권 책을 쓰는지?"</li>
        </ol>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="right-wrap">', unsafe_allow_html=True)
    st.markdown('<div class="right-menu">⋮</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="hero-shell">
            <div class="hero-icon-box">
                <div class="hero-icon">🧙</div>
            </div>
            <div class="hero-title">1주일에 한 권, 슈퍼AI급 책쓰기법</div>
            <div class="hero-author">By <strong>AI 최대표</strong></div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="input-fixed"><div class="input-shell">', unsafe_allow_html=True)

topic = st.text_input(
    "메시지 입력",
    placeholder="Your message",
    label_visibility="collapsed"
)

st.markdown('<div class="send-btn-wrap">', unsafe_allow_html=True)
generate = st.button("➤")
st.markdown('</div></div></div>', unsafe_allow_html=True)

if generate:
    if not topic.strip():
        st.warning("주제를 입력해줘.")
    else:
        prompt = f"""
너는 전자책 전문 작가이자 책쓰기 코치다.

사용자가 입력한 주제:
{topic}

아래 형식으로 한국어 전자책 초안을 길고 풍부하게 작성해라.

조건:
- 제목 3개 제안
- 가장 좋은 제목 1개 선정
- 한 줄 소개
- 프롤로그
- 목차
- 1장~5장
- 각 장마다 소제목 3개 이상
- 각 소제목은 초보자도 이해하기 쉽게 자세히 설명
- 예시, 실전 팁, 적용 포인트 포함
- 마지막에 FAQ 5개
- 마지막에 실행 체크리스트 10개
- 전체적으로 실제 전자책 원고처럼 자연스럽고 풍부하게 작성

출력은 읽기 좋은 실제 원고 스타일로 정리해라.
"""
        try:
            with st.spinner("전자책 초안 작성 중..."):
                response = client.responses.create(
                    model="gpt-4o-mini",
                    input=prompt
                )
                st.session_state.result = response.output_text
        except Exception as e:
            st.session_state.result = f"오류가 발생했어.\n\n{str(e)}"

if st.session_state.result:
    safe_result = (
        st.session_state.result
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )

    st.markdown(f"""
    <div class="result-shell">
        <div class="result-title">생성된 초안</div>
        <div class="result-box">{safe_result}</div>
        <div class="download-wrap"></div>
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        "전자책 초안 다운로드",
        st.session_state.result,
        file_name="ebook_draft.txt",
        mime="text/plain"
    )
