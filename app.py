import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI 전자책 생성기", page_icon="📘", layout="centered")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📘 AI 전자책 생성기")
st.write("주제를 입력하면 AI가 전자책 초안을 자동으로 작성해줍니다.")

topic = st.text_input("주제를 입력하세요", placeholder="예: AI 자동수익 만드는 방법")

if st.button("전자책 생성"):
    if topic.strip() == "":
        st.warning("주제를 입력하세요")
    else:
        with st.spinner("AI가 전자책을 작성 중입니다..."):
            prompt = f"""
너는 전자책 전문가다.

주제: {topic}

아래 구조로 전자책을 작성해라.

1. 제목
2. 소개
3. 목차
4. 챕터별 내용
5. 마무리

조건:
- 초보자가 이해하기 쉽게 작성
- 문장은 너무 어렵지 않게 작성
- 바로 실행할 수 있도록 실전형으로 작성
- 각 항목은 보기 좋게 정리
- 한국어로 자연스럽게 작성
"""

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "user", "content": prompt}
                ],
            )

            result = response.choices[0].message.content

            st.success("전자책 초안이 완성되었습니다!")
            st.text_area("전자책 결과", result, height=500)
            st.download_button(
                "텍스트 다운로드",
                result,
                file_name="ebook.txt",
                mime="text/plain"
            )
