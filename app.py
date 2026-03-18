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

    text = re.sub(r"[^\x00-\xFF가-힣ㄱ-ㅎㅏ-ㅣ\n\r\t ]", "", text)
    return text


def make_pdf(text: str) -> str:
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    font_path = "/usr/share/fonts/truetype/nanum/NanumGothic.ttf"

    if os.path.exists(font_path):
        pdf.add_font("Nanum", "", font_path)
        pdf.set_font("Nanum", size=12)
    else:
        pdf.set_font("Arial", size=12)
        text = clean_text_for_pdf(text)

    for paragraph in text.split("\n"):
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

                pdf_path = make_pdf(result)
                with open(pdf_path, "rb") as f:
                    st.download_button(
                        "📘 PDF 다운로드",
                        f,
                        file_name="ebook.pdf",
                        mime="application/pdf"
                    )

            except Exception as e:
                st.error("생성 중 오류가 발생했습니다.")
                st.error(str(e))
                st.info("OpenAI 결제/한도 문제이거나 모델 사용 제한일 수 있어요. 잠시 후 다시 시도해보세요.")
