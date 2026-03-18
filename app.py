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
    background: #050914;
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

section.main,
section.main > div,
.block-container,
[data-testid="stAppViewContainer"] {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

.block-container {
    max-width: 100vw !important;
    padding: 0 !important;
}

/* streamlit 기본 wrapper들 최소화 */
div[data-testid="stVerticalBlock"] {
    gap: 0 !important;
}

/* ===== 전체 레이아웃 ===== */
.app-shell {
    width: 100vw;
    height: 100vh;
    display: flex;
    background:
        radial-gradient(circle at 70% 40%, rgba(31, 63, 130, 0.18) 0%, rgba(4, 8, 20, 0) 28%),
        linear-gradient(180deg, #030712 0%, #020611 100%);
    overflow: hidden;
}

/* ===== 왼쪽 패널 ===== */
.left-panel {
    width: 390px;
    min-width: 390px;
    height: 100vh;
    background: linear-gradient(180deg, rgba(45,46,58,0.96) 0%, rgba(36,38,49,0.97) 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
    padding: 28px 28px 28px 28px;
    box-sizing: border-box;
    position: relative;
}

.close-x {
    position: absolute;
    top: 16px;
    right: 18px;
    color: rgba(255,255,255,0.88);
    font-size: 24px;
    line-height: 1;
    font-weight: 400;
}

.left-title {
    color: #ffffff;
    font-size: 24px;
    font-weight: 800;
    line-height: 1.45;
    margin-top: 72px;
    margin-bottom: 34px;
    word-break: keep-all;
}

.left-dot {
    color: #ffffff;
    font-size: 17px;
    line-height: 1.8;
    margin-bottom: 22px;
    font-weight: 700;
}

.left-list {
    margin: 0;
    padding-left: 34px;
}

.left-list li {
    color: #ffffff;
    font-size: 18px;
    line-height: 1.7;
    margin-bottom: 10px;
    font-weight: 700;
    word-break: keep-all;
}

/* ===== 오른쪽 메인 ===== */
.right-panel {
    flex: 1;
    height: 100vh;
    position: relative;
    overflow: hidden;
    background:
        radial-gradient(circle at 50% 22%, rgba(37, 66, 128, 0.16) 0%, rgba(5,9,20,0) 18%),
        linear-gradient(180deg, #020714 0%, #030814 100%);
}

.menu-dots {
    position: absolute;
    top: 14px;
    right: 20px;
    color: rgba(255,255,255,0.88);
    font-size: 28px;
    letter-spacing: 1px;
    z-index: 5;
}

.main-center {
    height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 40px 32px 140px 32px;
    box-sizing: border-box;
    text-align: center;
}

.hero-icon-wrap {
    width: 250px;
    height: 250px;
    border-radius: 24px;
    margin-bottom: 26px;
    position: relative;
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
    opacity: 0.92;
}

.hero-icon {
    font-size: 126px;
    filter: grayscale(1) brightness(0.72);
}

.hero-title {
    color: #ffffff;
    font-size: 62px;
    font-weight: 900;
    letter-spacing: -0.03em;
    line-height: 1.18;
    margin-bottom: 14px;
    word-break: keep-all;
}

.hero-author {
    color: #c1c9da;
    font-size: 16px;
}

.hero-author span {
    color: #ffffff;
    font-weight: 700;
}

/* ===== 입력창 ===== */
.input-fixed {
    position: fixed;
    left: calc(390px + ((100vw - 390px) / 2));
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

.send-button {
    position: absolute;
    right: 10px;
    top: 12px;
    width: 46px;
    height: 40px;
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
    left: 422px;
    right: 28px;
    bottom: 110px;
    max-height: 42vh;
    overflow: auto;
    background: rgba(12, 17, 30, 0.90);
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

/* ===== 모바일 대응 ===== */
@media (max-width: 1100px) {
    .left-panel {
        display: none;
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

    .hero-title {
        font-size: 42px;
    }

    .hero-icon-wrap {
        width: 200px;
        height: 200px;
    }

    .hero-icon {
        font-size: 100px;
    }

    .main-center {
        padding-left: 20px;
        padding-right: 20px;
        padding-bottom: 130px;
    }
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="app-shell">
    <div class="left-panel">
        <div class="close-x">×</div>
        <div class="left-title">
            하루에 책 한권을 쓰는 챗쓰기의 신 등장, 그 이름은 바로 AI 책쓰기의 신!
        </div>
        <div class="left-dot">• 사용 예시 :</div>
        <ol class="left-list">
            <li>"효율적으로 글을 쓰는 방법은?"</li>
            <li>"책으로 독자들에게 감동을 주는 방법은?"</li>
            <li>"어떻게 하루 1권 책을 쓰는지?"</li>
        </ol>
    </div>

    <div class="right-panel">
        <div class="menu-dots">⋮</div>
        <div class="main-center">
            <div class="hero-icon-wrap">
                <div class="hero-icon">🧙</div>
            </div>
            <div class="hero-title">1주일에 한 권, 슈퍼AI급 책쓰기법</div>
            <div class="hero-author">By <span>AI 최대표</span></div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-fixed"><div class="input-shell">', unsafe_allow_html=True)

topic = st.text_input(
    "메시지 입력",
    placeholder="Your message",
    label_visibility="collapsed"
)

st.markdown('<div class="send-button">', unsafe_allow_html=True)
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

출력은 마크다운 느낌보다 실제 원고처럼 읽기 좋게 정리해라.
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
