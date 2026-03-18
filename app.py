import os
import re
import tempfile

import streamlit as st
from openai import OpenAI
from fpdf import FPDF

st.set_page_config(
    page_title="AI 전자책 생성기",
    page_icon="📘",
    layout="centered"
)

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📘 AI 전자책 생성기")
st.write("주제를 입력하면 AI가 전자책 초안을 만들고, TXT/PDF로 다운로드할 수 있어요.")

st.markdown("""
### 하루 1시간, AI로 전자책 자동 생성

✔ 초보자도 쉽게 사용 가능  
✔ 전자책 초안 자동 생성  
✔ TXT / PDF 다운로드 가능  
""")

topic = st.text_input(
    "주제를 입력하세요",
    placeholder="예: AI 자동수익 만드는 방법"
)

tone = st.selectbox(
    "말투를 선택하세요",
    ["친근한 말투", "전문가형", "마케팅형"]
)

length = st.selectbox(
    "분량 느낌",
    ["짧게", "보통", "길게"]
)


def clean_text_for_pdf(text: str) -> str:
    replacements = {
        "📘": "[전자책]",
        "✅": "-",
        "✔": "-",
        "👉": "->",
        "•": "-",
        "—": "-",
        "–": "-",
        "“": '"',
        "”": '"',
        "‘": "'",
        "’": "'",
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    return text


def make_pdf(text: str) -> str:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Streamlit Cloud에서 자주 되는 한글 폰트 경로들
    possible_fonts = [
        "/usr/share/fonts/truetype/nanum/NanumGothic.ttf",
        "/usr/share/fonts/truetype/noto/NotoSansCJK-Regular.ttc",
        "/usr/share/fonts/truetype/noto/NotoSansCJKkr-Regular.otf",
    ]

    font_path = None
    for path in possible_fonts:
        if os.path.exists(path):
            font_path = path
            break

    if font_path:
        pdf.add_font("KoreanFont", "", font_path, uni=True)
        pdf.set_font("KoreanFont", size=12)
        safe_text = text
    else:
        # 한글 폰트가 없으면 PDF에서 한글이 깨지므로 최소 안전처리
        pdf.set_font("Helvetica", size=12)
        safe_text = clean_text_for_pdf(text)
        safe_text = re.sub(r"[가-힣ㄱ-ㅎㅏ-ㅣ]", "?", safe_text)

    for paragraph in safe_text.split("\n"):
        if not paragraph.strip():
            pdf.ln(4)
            continue
        pdf.multi_cell(0, 8, paragraph)

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
    pdf.output(temp_file.name)
    return temp_file.name


if st.button("전자책 생성"):
    if topic.strip() == "":
        st.warning("주제를 입력하세요.")
    else:
        with st.spinner("AI가 전자책을 작성 중입니다..."):
            prompt = f"""
너는 전자책 전문 작가다.

주제: {topic}
말투: {tone}
분량: {length}

아래 형식으로 한국어 전자책 초안을 작성해라.

[출력 형식]
1. 전자책 제목
2. 한 줄 소개
3. 목차
4. 본문
   - 1장
   - 2장
   - 3장
   - 4장
   - 5장
5. 마무리
6. 바로 실행할 수 있는 체크리스트

[작성 조건]
- 초보자도 이해하기 쉽게 작성
- 너무 어려운 표현 금지
- 실전형으로 작성
- 문단은 짧게
- 보기 좋게 구분
- 한국어로 자연스럽게 작성
- 바로 복사해서 전자책 초안으로 쓸 수 있게 작성
- 너무 길지 않게 적당한 분량으로 작성
"""

            try:
                response = client.responses.create(
                    model="gpt-4o-mini",
                    input=prompt
                )

                result = response.output_text

                st.success("전자책 초안이 완성되었습니다!")

                st.text_area("전자책 결과", result, height=500)

                st.download_button(
                    "텍스트 다운로드",
                    result,
                    file_name="ebook.txt",
                    mime="text/plain"
                )

                try:
                    pdf_path = make_pdf(result)
                    with open(pdf_path, "rb") as f:
                        st.download_button(
                            "📘 PDF 다운로드",
                            f,
                            file_name="ebook.pdf",
                            mime="application/pdf"
                        )
                except Exception as pdf_error:
                    st.warning("PDF 생성에서만 오류가 났어요. 텍스트 다운로드는 정상 사용 가능해요.")
                    st.error(str(pdf_error))

            except Exception as e:
                st.error("생성 중 오류가 발생했습니다.")
                st.error(str(e))
                st.info("OpenAI 결제/한도 문제이거나 모델 사용 제한일 수 있어요. 잠시 후 다시 시도해보세요.")
