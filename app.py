import streamlit as st
from openai import OpenAI

st.set_page_config(
    page_title="AI 책쓰기 스튜디오",
    page_icon="📘",
    layout="wide"
)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# -----------------------------
# 상태 저장
# -----------------------------
if "result" not in st.session_state:
    st.session_state.result = ""

# -----------------------------
# 스타일 (여백 제거 포함)
# -----------------------------
st.markdown("""
<style>

/* 🔥 상단 공백 제거 핵심 */
.block-container {
    max-width: 1500px;
    padding: 0rem !important;
}

section.main {
    padding-top: 0rem !important;
}

.css-18e3th9 {
    padding-top: 0rem !important;
}

section.main > div {
    padding-top: 0rem !important;
}

div[data-testid="stVerticalBlock"] {
    gap: 0rem !important;
}

/* ------------------- 기본 스타일 ------------------- */

html, body {
    font-family: "Pretendard", "Noto Sans KR", sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #060914 0%, #080c18 100%);
}

/* 좌측 */
.left-panel {
    background: rgba(255,255,255,0.05);
    border-radius: 20px;
    padding: 24px;
    height: 100vh;
}

/* 우측 */
.right-panel {
    background: radial-gradient(circle at top, rgba(19,38,92,0.35) 0%, rgba(7,11,22,0.96) 65%);
    border-radius: 20px;
    padding: 40px;
    height: 100vh;
}

.hero-title {
    font-size: 48px;
    font-weight: 800;
    color: white;
    text-align: center;
}

.hero-sub {
    color: #bfc8e0;
    text-align: center;
    margin-bottom: 30px;
}

.stButton > button {
    width: 100%;
    height: 50px;
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# 레이아웃
# -----------------------------
left, right = st.columns([1,2])

with left:
    st.markdown('<div class="left-panel">', unsafe_allow_html=True)

    st.markdown("### 하루에 한 권 초안 만들기")

    st.write("이건 단순 글 생성기가 아니라")
    st.write("전자책 초안을 빠르게 만드는 툴입니다.")

    st.markdown("#### 사용 예시")

    st.write("1. 온라인 부업 전자책")
    st.write("2. 인스타 수익화 전자책")
    st.write("3. AI 자동화 전자책")

    st.markdown('</div>', unsafe_allow_html=True)

with right:
    st.markdown('<div class="right-panel">', unsafe_allow_html=True)

    st.markdown('<div class="hero-title">AI 책쓰기 스튜디오</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-sub">전자책 초안을 자동으로 생성합니다</div>', unsafe_allow_html=True)

    topic = st.text_input("주제 입력")

    tone = st.selectbox("말투", ["친근한", "전문가형"])
    length = st.selectbox("분량", ["길게", "아주 길게"])

    if st.button("전자책 생성"):

        if topic == "":
            st.warning("주제 입력하세요")

        else:
            prompt = f"""
주제: {topic}
말투: {tone}
분량: {length}

전자책 형태로 길고 자세하게 작성해라.

구성:
제목 / 프롤로그 / 목차 / 1~5장 / 마무리 / FAQ / 체크리스트

절대 짧게 쓰지마라.
"""

            with st.spinner("작성중..."):
                try:
                    response = client.responses.create(
                        model="gpt-4o-mini",
                        input=prompt
                    )

                    st.session_state.result = response.output_text

                except Exception as e:
                    st.error("오류 발생")
                    st.write(e)

    if st.session_state.result:
        st.text_area("결과", st.session_state.result, height=500)

        st.download_button(
            "다운로드",
            st.session_state.result,
            file_name="ebook.txt"
        )

    st.markdown('</div>', unsafe_allow_html=True)
