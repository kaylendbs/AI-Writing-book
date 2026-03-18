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

st.markdown("""
<style>
/* 전체 기본 */
html, body, [class*="css"] {
    font-family: "Pretendard", "Noto Sans KR", sans-serif;
}

.stApp {
    background: linear-gradient(180deg, #050814 0%, #060b1d 100%);
}

/* 상단 공백 제거 */
.block-container {
    max-width: 1500px !important;
    padding-top: 0rem !important;
    padding-bottom: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

section.main > div {
    padding-top: 0rem !important;
}

/* 컬럼 간격 */
div[data-testid="stHorizontalBlock"] {
    gap: 24px !important;
}

/* 각 컬럼을 카드처럼 */
div[data-testid="column"]:nth-of-type(1) {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 24px;
    padding: 28px 24px 28px 24px;
    min-height: 92vh;
}

div[data-testid="column"]:nth-of-type(2) {
    background: radial-gradient(circle at top, rgba(22,37,92,0.30) 0%, rgba(7,11,22,0.96) 62%);
    border: 1px solid rgba(255,255,255,0.07);
    border-radius: 24px;
    padding: 36px 36px 28px 36px;
    min-height: 92vh;
}

/* 텍스트 */
.hero-icon {
    text-align: center;
    font-size: 72px;
    margin-top: 6px;
    margin-bottom: 8px;
}

.hero-title {
    text-align: center;
    color: white;
    font-size: 56px;
    font-weight: 800;
    line-height: 1.1;
    margin-bottom: 10px;
}

.hero-sub {
    text-align: center;
    color: #c4cbe0;
    font-size: 17px;
    line-height: 1.7;
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
    line-height: 1.25;
    margin-bottom: 14px;
}

.left-body {
    color: #dce3f3;
    font-size: 16px;
    line-height: 1.9;
    margin-bottom: 18px;
}

.left-muted {
    color: #aeb8cf;
    font-size: 15px;
    line-height: 1.9;
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

/* 입력창 */
div[data-testid="stTextInput"] input {
    background: rgba(255,255,255,0.06) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 14px !important;
    color: white !important;
    min-height: 54px !important;
}

div[data-testid="stSelectbox"] > div {
    background: rgba(255,255,255,0.06) !important;
    border-radius: 14px !important;
}

.stButton > button {
    width: 100% !important;
    min-height: 54px !important;
    border-radius: 14px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    background: linear-gradient(180deg, #131c34 0%, #0b1020 100%) !important;
    color: white !important;
    font-size: 16px !important;
    font-weight: 700 !important;
}

div[data-testid="stTextArea"] textarea {
    background: rgba(255,255,255,0.05) !important;
    color: white !important;
    border-radius: 16px !important;
    line-height: 1.8 !important;
}

.stDownloadButton > button {
    width: 100% !important;
    min-height: 52px !important;
    border-radius: 14px !important;
    font-weight: 700 !important;
}

/* 라벨 */
label, .stSelectbox label, .stTextInput label {
    color: #dce4f6 !important;
    font-weight: 700 !important;
}
</style>
""", unsafe_allow_html=True)

left, right = st.columns([1, 2.2])

with left:
    st.markdown('<div class="left-title">하루에 한 권 초안 만들기</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="left-body">이 공간은 단순한 글 생성기가 아니라<br>전자책 초안을 빠르게 만드는 책쓰기 툴입니다.</div>',
        unsafe_allow_html=True
    )

    st.markdown('<div class="left-title" style="font-size:28px; margin-top:28px;">사용 예시</div>', unsafe_allow_html=True)
    st.markdown("""
<div class="left-body">
1. "효율적으로 글을 쓰는 방법 전자책 써줘"<br><br>
2. "초보도 가능한 온라인 부업 전자책 써줘"<br><br>
3. "AI 자동화로 수익 만드는 방법 전자책 써줘"<br><br>
4. "인스타 수익화 입문 가이드 전자책 써줘"<br><br>
5. "퇴사 후 1인 온라인 수익 만들기 전자책 써줘"
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div class="left-muted">
주제는 조금 구체적으로 적을수록 결과가 더 좋아집니다.<br>
예: "초보 주부도 가능한 블로그 수익화 입문서"
</div>
""", unsafe_allow_html=True)

    st.markdown("""
<div style="margin-top:22px;">
<span class="badge">전자책 초안</span>
<span class="badge">긴 원고 생성</span>
<span class="badge">초보자용</span>
<span class="badge">다운로드 가능</span>
<span class="badge">다크 UI</span>
</div>
""", unsafe_allow_html=True)

with right:
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

    topic = st.text_input(
        "주제 입력",
        placeholder="예: 초보도 가능한 온라인 부업 / AI 자동화 수익 / 인스타 수익화 입문"
    )

    col1, col2 = st.columns(2)
    with col1:
        tone = st.selectbox("말투", ["친근한 말투", "전문가형", "마케팅형"])
    with col2:
        reader = st.selectbox("대상", ["초보자", "직장인", "부업 입문자", "1인사업 준비자"])

    col3, col4 = st.columns(2)
    with col3:
        length = st.selectbox("분량", ["길게", "아주 길게"])
    with col4:
        structure = st.selectbox("스타일", ["실전형", "가이드형", "설득형"])

    if st.button("전자책 생성"):
        if topic.strip() == "":
            st.warning("주제를 입력해주세요.")
        else:
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
- 전자책 원고처럼 복붙해서 바로 쓸 수 있게 써라.

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

    if st.session_state.result:
        st.text_area("전자책 원고", st.session_state.result, height=720)

        st.download_button(
            "텍스트 다운로드",
            st.session_state.result,
            file_name="ebook.txt",
            mime="text/plain"
        )
