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
    background: linear-gradient(180deg, #030713 0%, #020611 100%);
}

/* ===== 기본 UI 숨기기 ===== */
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

div[data-testid="stHorizontalBlock"] {
    gap: 0 !important;
}

/* ===== 메인 프레임 ===== */
.app-frame {
    width: 100%;
    min-height: 100vh;
}

/* ===== 좌측 패널 ===== */
.left-panel {
    min-height: 100vh;
    background: linear-gradient(180deg, rgba(46,48,61,0.98) 0%, rgba(35,37,49,0.98) 100%);
    border-right: 1px solid rgba(255,255,255,0.06);
    padding: 22px 28px 36px 28px;
    box-sizing: border-box;
}

.left-top {
    display: flex;
    justify-content: flex-end;
    color: rgba(255,255,255,0.88);
    font-size: 32px;
    line-height: 1;
    margin-bottom: 46px;
}

.left-title {
    color: #ffffff;
    font-size: 27px;
    font-weight: 800;
    line-height: 1.42;
    word-break: keep-all;
    margin-bottom: 28px;
}

.left-sub {
    color: #ffffff;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 16px;
}

.left-list {
    color: #ffffff;
    font-size: 17px;
    line-height: 1.75;
    font-weight: 700;
    padding-left: 30px;
    margin: 0;
}

.left-list li {
    margin-bottom: 12px;
}

/* ===== 우측 패널 ===== */
.right-panel {
    min-height: 100vh;
    position: relative;
    background:
        radial-gradient(circle at 50% 24%, rgba(42, 72, 142, 0.16) 0%, rgba(5,9,20,0) 18%),
        linear-gradient(180deg, #020714 0%, #020611 100%);
    overflow: hidden;
}

.right-menu {
    position: absolute;
    top: 16px;
    right: 22px;
    color: rgba(255,255,255,0.88);
    font-size: 28px;
    z-index: 5;
}

.hero-shell {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 40px 30px 140px 30px;
    box-sizing: border-box;
}

.hero-inner {
    width: 100%;
    max-width: 980px;
    margin: 0 auto;
}

.hero-icon-box {
    width: 240px;
    height: 240px;
    margin: 0 auto 24px auto;
    border-radius: 24px;
    background:
        repeating-linear-gradient(
            135deg,
            rgba(255,255,255,0.016) 0px,
            rgba(255,255,255,0.016) 2px,
            transparent 2px,
            transparent 10px
        );
    display: flex;
    align-items: center;
    justify-content: center;
}

.hero-icon {
    font-size: 112px;
    filter: grayscale(1) brightness(0.75);
}

.hero-title {
    color: #ffffff;
    font-size: 58px;
    font-weight: 900;
    line-height: 1.18;
    letter-spacing: -0.03em;
    margin-bottom: 14px;
    word-break: keep-all;
}

.hero-author {
    color: #c4ccdc;
    font-size: 16px;
}

.hero-author strong {
    color: #ffffff;
    font-weight: 700;
}

/* ===== 입력창 ===== */
.input-fixed {
    position: fixed;
    left: calc(29% + ((71%) / 2));
    transform: translateX(-50%);
    bottom: 28px;
    width: min(820px, calc(100vw - 470px));
    z-index: 50;
}

.input-shell {
    position: relative;
    width: 100%;
}

div[data-testid="stTextInput"] {
    margin: 0 !important;
}

div[data-testid="stTextInput"] input {
    height: 64px !important;
    min-height: 64px !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.06) !important;
    background: rgba(49, 53, 69, 0.84) !important;
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
    z-index: 60;
}

.stButton > button {
    width: 46px !important;
    min-width: 46px !important;
    height: 40px !important;
    min-height: 40px !important;
    border-radius: 10px !important;
    border: none !important;
    background: rgba(255,255,255,0.09) !important;
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
    left: 31%;
    right: 28px;
    bottom: 108px;
    max-height: 42vh;
    overflow: auto;
    background: rgba(11, 16, 29, 0.94);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 22px 24px;
    box-sizing: border-box;
    backdrop-filter: blur(10px);
    z-index: 40;
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

.download-inline {
    margin-top: 16px;
}

div[data-testid="stDownloadButton"] > button {
    width: 100% !important;
    height: 48px !important;
    min-height: 48px !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    background: rgba(255,255,255,0.05) !important;
    color: #ffffff !important;
    font-weight: 700 !important;
}

/* ===== 모바일 ===== */
@media (max-width: 1100px) {
    .left-panel {
        display: none;
    }

    .hero-shell {
        padding: 40px 20px 130px 20px;
    }

    .hero-title {
        font-size: 40px;
    }

    .hero-icon-box {
        width: 190px;
        height: 190px;
    }

    .hero-icon {
        font-size: 92px;
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

st.markdown('<div class="app-frame">', unsafe_allow_html=True)

left, right = st.columns([1.08, 2.42], gap="small")

with left:
    st.markdown("""
    <div class="left-panel">
        <div class="left-top">×</div>
        <div class="left-title">
            하루에 책 한권을 쓰는 챗쓰기의 신 등장, 그 이름은 바로 AI 책쓰기의 신!
        </div>
        <div class="left-sub">• 사용 예시 :</div>
        <ol class="left-list">
            <li>"효율적으로 글을 쓰는 방법은?"</li>
            <li>"책으로 독자들에게 감동을 주는 방법은?"</li>
            <li>"어떻게 하루 1권 책을 쓰는지?"</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)

with right:
    st.markdown("""
    <div class="right-panel">
        <div class="right-menu">⋮</div>
        <div class="hero-shell">
            <div class="hero-inner">
                <div class="hero-icon-box">
                    <div class="hero-icon">🧙</div>
                </div>
                <div class="hero-title">1주일에 한 권, 슈퍼AI급 책쓰기법</div>
                <div class="hero-author">By <strong>AI 최대표</strong></div>
            </div>
        </div>
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

사용자 주제:
{topic}

다음 조건으로 한국어 전자책 초안을 작성해라.

조건:
- 제목 3개 제안
- 최종 제목 1개 선정
- 한 줄 소개
- 프롤로그
- 목차
- 1장~5장
- 각 장마다 소제목 3개 이상
- 각 소제목은 초보자도 이해하기 쉽게 자세히 설명
- 예시, 실전 팁, 적용 포인트 포함
- FAQ 5개
- 실행 체크리스트 10개
- 전체적으로 실제 전자책 원고처럼 길고 풍부하게 작성
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
        <div class="download-inline"></div>
    </div>
    """, unsafe_allow_html=True)

    st.download_button(
        "전자책 초안 다운로드",
        st.session_state.result,
        file_name="ebook_draft.txt",
        mime="text/plain"
    )
