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

if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

# -----------------------------
# 커스텀 스타일
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    font-family: "Pretendard", "Noto Sans KR", sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #060914 0%, #080c18 100%);
}

.block-container {
    max-width: 1500px;
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.main-wrap {
    background: transparent;
}

.left-panel {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 22px;
    padding: 28px 24px;
    min-height: 760px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.18);
}

.right-panel {
    position: relative;
    background: radial-gradient(circle at top, rgba(19,38,92,0.35) 0%, rgba(7,11,22,0.96) 65%);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 28px;
    padding: 40px 42px 28px 42px;
    min-height: 760px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.18);
    overflow: hidden;
}

.hero-icon {
    font-size: 82px;
    text-align: center;
    margin-top: 18px;
    margin-bottom: 18px;
    opacity: 0.95;
}

.hero-title {
    text-align: center;
    font-size: 56px;
    line-height: 1.15;
    font-weight: 800;
    color: white;
    margin-top: 18px;
    margin-bottom: 12px;
}

.hero-sub {
    text-align: center;
    color: #c7cfdf;
    font-size: 17px;
    line-height: 1.75;
    margin-bottom: 28px;
}

.hero-mini {
    text-align: center;
    color: #97a1b5;
    font-size: 14px;
    margin-bottom: 32px;
}

.section-title {
    font-size: 30px;
    font-weight: 800;
    color: white;
    margin-bottom: 14px;
}

.section-body {
    color: #eef2ff;
    font-size: 16px;
    line-height: 1.9;
}

.muted {
    color: #b8c1d6;
    font-size: 15px;
    line-height: 1.9;
}

.tip-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 16px;
    padding: 14px 16px;
    margin-top: 16px;
    margin-bottom: 16px;
}

.badge {
    display: inline-block;
    padding: 8px 12px;
    margin: 6px 6px 0 0;
    border-radius: 999px;
    background: rgba(255,255,255,0.06);
    border: 1px solid rgba(255,255,255,0.08);
    color: #e9eefb;
    font-size: 13px;
}

.result-shell {
    margin-top: 18px;
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 18px;
}

.footer-note {
    color: #95a0b8;
    font-size: 13px;
    margin-top: 14px;
}

div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    color: white !important;
    min-height: 54px;
}

div[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 16px !important;
    color: white !important;
    line-height: 1.8 !important;
}

div[data-testid="stSelectbox"] > div {
    background: rgba(255,255,255,0.06);
    border-radius: 14px;
}

.stButton > button {
    width: 100%;
    min-height: 54px;
    border-radius: 16px;
    border: 1px solid rgba(255,255,255,0.08);
    background: linear-gradient(180deg, #11182e 0%, #0b1021 100%);
    color: white;
    font-weight: 700;
    font-size: 16px;
}

.stDownloadButton > button {
    width: 100%;
    min-height: 52px;
    border-radius: 14px;
    background: rgba(255,255,255,0.06);
    color: white;
    border: 1px solid rgba(255,255,255,0.08);
    font-weight: 700;
}

.block-label {
    color: #c6cde0;
    font-size: 14px;
    margin-bottom: 6px;
    margin-top: 12px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 레이아웃
# -----------------------------
left_col, right_col = st.columns([1, 2.3], gap="large")

with left_col:
    st.markdown('<div class="left-panel">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">하루에 한 권 초안 만들기</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="section-body">
이 공간은 단순한 글 생성기가 아니라<br>
<b>전자책 초안을 빠르게 만드는 책쓰기 툴</b>입니다.
</div>
""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("""
<div class="muted">
• 사용 예시
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="section-body">
1. "효율적으로 글을 쓰는 방법 전자책 써줘"<br><br>
2. "초보도 가능한 온라인 부업 전자책 써줘"<br><br>
3. "AI 자동화로 수익 만드는 방법 전자책 써줘"<br><br>
4. "인스타 수익화 입문 가이드 전자책 써줘"<br><br>
5. "퇴사 후 1인 온라인 수익 만들기 전자책 써줘"
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="tip-box">
<div class="muted"><b>추천 활용법</b></div>
<div class="section-body">
주제는 넓게 쓰는 것보다<br>
조금 구체적으로 넣을수록 결과가 더 좋아집니다.
</div>
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="badge">전자책 초안</div>
<div class="badge">긴 원고 생성</div>
<div class="badge">초보자용</div>
<div class="badge">다운로드 가능</div>
<div class="badge">다크 모드 UI</div>
""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

with right_col:
    st.markdown('<div class="right-panel">', unsafe_allow_html=True)

    st.markdown('<div class="hero-icon">🧠</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">AI 책쓰기 스튜디오</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="hero-sub">짧은 답변이 아니라, 제목 · 프롤로그 · 목차 · 5개 장 · FAQ · 체크리스트까지 포함된<br>전자책 초안을 길고 풍부하게 생성합니다.</div>',
        unsafe_allow_html=True
    )
    st.markdown(
        '<div class="hero-mini">복붙해서 전자책 초안으로 바로 쓸 수 있는 형태로 설계된 버전입니다.</div>',
        unsafe_allow_html=True
    )

    col_a, col_b, col_c = st.columns([2.2, 1, 1])

    with col_a:
        topic = st.text_input(
            "주제 입력",
            placeholder="예: 초보도 가능한 온라인 부업 / AI 자동화 수익 / 인스타 수익화 입문"
        )

    with col_b:
        tone = st.selectbox(
            "말투",
            ["친근한 말투", "전문가형", "마케팅형"]
        )

    with col_c:
        reader = st.selectbox(
            "대상",
            ["초보자", "직장인", "부업 입문자", "1인사업 준비자"]
        )

    col_d, col_e = st.columns([1, 1])

    with col_d:
        length = st.selectbox(
            "분량",
            ["길게", "아주 길게"]
        )

    with col_e:
        structure = st.selectbox(
            "스타일",
            ["실전형", "가이드형", "설득형"]
        )

    generate = st.button("전자책 생성")

    if generate:
        if topic.strip() == "":
            st.warning("주제를 입력해주세요.")
        else:
            st.session_state.last_topic = topic

            prompt = f"""
너는 전자책 전문 작가이자 콘텐츠 기획자다.

주제: {topic}
말투: {tone}
대상 독자: {reader}
구성 스타일: {structure}
분량 수준: {length}

아래 조건에 맞춰 한국어 전자책 초안을 작성해라.

[중요]
- 절대 짧게 쓰지 마라.
- 결과는 실제 전자책 초안처럼 길고 자세해야 한다.
- 최소 5개 장으로 구성해라.
- 각 장마다 최소 3개의 소제목을 넣어라.
- 각 소제목마다 최소 2~4문단 설명을 써라.
- 초보자가 읽어도 이해되게 쉽게 설명해라.
- 실전형 내용과 예시를 자주 넣어라.
- 내용은 자연스럽고 읽기 쉽게 써라.
- 너무 딱딱하지 않게, 하지만 허술하지 않게 써라.
- 전자책 원고처럼 복붙해서 바로 쓸 수 있게 써라.
- 내용이 빈약해 보이지 않게 풍부하게 작성해라.

[출력 형식]
# 전자책 제목
# 한 줄 소개
# 프롤로그
# 목차

# 1장
## 소제목
내용

## 소제목
내용

## 소제목
내용

# 2장
## 소제목
내용

## 소제목
내용

## 소제목
내용

# 3장
## 소제목
내용

## 소제목
내용

## 소제목
내용

# 4장
## 소제목
내용

## 소제목
내용

## 소제목
내용

# 5장
## 소제목
내용

## 소제목
내용

## 소제목
내용

# 마무리
# 자주 묻는 질문 5개
# 바로 실행 체크리스트 10개

[추가 지시]
- 제목은 판매 가능한 전자책처럼 매력적으로 써라.
- 프롤로그는 독자의 고민을 공감하는 방식으로 써라.
- 목차는 번호로 정리해라.
- 각 장은 확실히 구분되게 써라.
- 각 장의 내용은 너무 짧지 않게 풍부하게 써라.
- 한국어로만 자연스럽게 작성해라.
"""

            try:
                with st.spinner("AI가 전자책을 작성 중입니다..."):
                    response = client.responses.create(
                        model="gpt-4o-mini",
                        input=prompt
                    )

                    st.session_state.result = response.output_text

                st.success("전자책 초안이 완성되었습니다.")

            except Exception as e:
                st.error("생성 중 오류가 발생했습니다.")
                st.error(str(e))
                st.info("OpenAI 결제/한도 또는 일시적 요청 제한 문제일 수 있어요. 잠시 후 다시 시도해보세요.")

    if st.session_state.result:
        st.markdown('<div class="result-shell">', unsafe_allow_html=True)
        st.markdown("#### 전자책 원고")
        st.text_area(
            "생성 결과",
            st.session_state.result,
            height=760
        )

        st.download_button(
            "텍스트 다운로드",
            st.session_state.result,
            file_name="ebook.txt",
            mime="text/plain"
        )

        st.markdown(
            '<div class="footer-note">생성된 결과는 초안입니다. 필요에 따라 제목, 문장, 사례를 추가로 다듬으면 훨씬 더 완성도 높게 사용할 수 있어요.</div>',
            unsafe_allow_html=True
        )
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
