import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI 책쓰기 스튜디오",
    page_icon="📘",
    layout="wide"
)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "result" not in st.session_state:
    st.session_state.result = ""

# ✅ 상단 여백 완전 제거 + UI 스타일
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Pretendard", "Noto Sans KR", sans-serif;
}

/* 🔥 상단 여백 제거 핵심 */
header {visibility:hidden;height:0;}
[data-testid="stToolbar"] {display:none;}
[data-testid="stHeader"] {display:none;}
[data-testid="stDecoration"] {display:none;}

.stApp {
    background: linear-gradient(180deg, #050814 0%, #060b1d 100%);
}

/* 전체 컨테이너 */
section.main, section.main > div {
    padding-top: 0rem !important;
    margin-top: 0rem !important;
}

.block-container {
    max-width: 1500px !important;
    padding-top: 0rem !important;
    margin-top: 0rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* 컬럼 간격 */
div[data-testid="stHorizontalBlock"] {
    gap: 24px !important;
}

/* 카드 */
div[data-testid="column"]:nth-of-type(1) {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 24px;
    padding: 28px 24px;
    min-height: 92vh;
}

div[data-testid="column"]:nth-of-type(2) {
    background: radial-gradient(circle at top, rgba(22,37,92,0.30) 0%, rgba(7,11,22,0.96) 62%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 24px;
    padding: 36px;
    min-height: 92vh;
}

/* 텍스트 */
.hero-icon {
    text-align: center;
    font-size: 72px;
    margin-top: 0;
    margin-bottom: 8px;
}

.hero-title {
    text-align: center;
    color: white;
    font-size: 56px;
    font-weight: 800;
    margin: 0;
}

.hero-sub {
    text-align: center;
    color: #c4cbe0;
    font-size: 17px;
    margin-bottom: 24px;
}

.hero-mini {
    text-align: center;
    color: #97a1b7;
    font-size: 14px;
    margin-bottom: 28px;
}

.left-title {
    color: white;
    font-size: 34px;
    font-weight: 800;
    margin-top: 0;
}

.left-body {
    color: #dce3f3;
    font-size: 16px;
    line-height: 1.9;
}

.left-muted {
    color: #aeb8cf;
    font-size: 15px;
}

.badge {
    display: inline-block;
    padding: 8px 12px;
    margin: 6px 6px 0 0;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    color: #eef2ff;
    font-size: 13px;
}

/* 입력 */
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 14px !important;
    color: white !important;
    min-height: 54px !important;
}

.stButton > button {
    width: 100% !important;
    min-height: 54px !important;
    border-radius: 14px !important;
    background: linear-gradient(180deg, #131c34 0%, #0b1020 100%) !important;
    color: white !important;
    font-weight: 700 !important;
}

div[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.05) !important;
    color: white !important;
    border-radius: 16px !important;
}

/* 라벨 */
label {
    color: #dce4f6 !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

left, right = st.columns([1, 2.2])

with left:
    st.markdown('<div class="left-title">하루에 한 권 초안 만들기</div>', unsafe_allow_html=True)
    st.markdown('<div class="left-body">전자책 초안을 빠르게 만드는 책쓰기 툴입니다.</div>', unsafe_allow_html=True)

    st.markdown('<div class="left-title" style="font-size:28px; margin-top:28px;">사용 예시</div>', unsafe_allow_html=True)

    st.markdown("""
<div class="left-body">
1. 온라인 부업 전자책<br><br>
2. AI 자동화 수익<br><br>
3. 인스타 수익화 가이드<br><br>
4. 1인 사업 시작법<br><br>
5. 퇴사 후 수익 만들기
</div>
""", unsafe_allow_html=True)

    st.markdown('<div class="left-muted">주제는 구체적일수록 좋습니다.</div>', unsafe_allow_html=True)

    st.markdown("""
<div style="margin-top:22px;">
<span class="badge">전자책</span>
<span class="badge">자동 생성</span>
<span class="badge">초보 가능</span>
</div>
""", unsafe_allow_html=True)

with right:
    st.markdown('<div class="hero-icon">🧠</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">AI 책쓰기 스튜디오</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">전자책 초안을 자동 생성합니다</div>', unsafe_allow_html=True)

    topic = st.text_input("주제 입력")

    if st.button("전자책 생성"):
        if topic.strip() == "":
            st.warning("주제를 입력해주세요.")
        else:
            with st.spinner("작성 중..."):
                response = client.responses.create(
                    model="gpt-4o-mini",
                    input=f"전자책 써줘: {topic}"
                )
                st.session_state.result = response.output_text

    if st.session_state.result:
        st.text_area("결과", st.session_state.result, height=600)

        st.download_button(
            "다운로드",
            st.session_state.result,
            file_name="ebook.txt"
        )
