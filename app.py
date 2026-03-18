import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="AI 전자책 생성기", page_icon="📘")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

st.title("📘 AI 전자책 생성기")

topic = st.text_input("주제를 입력하세요")

if st.button("전자책 생성"):
    if topic == "":
        st.warning("주제를 입력하세요")
    else:
        with st.spinner("AI가 전자책을 작성 중입니다..."):

            prompt = f"""
            너는 전자책 전문가다.

            주제: {topic}

            아래 구조로 전자책 작성:
            1. 제목
            2. 소개
            3. 목차
            4. 챕터별 내용

            초보자가 이해하기 쉽게 작성하고
            바로 실행할 수 있도록 작성해라.
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )

            result = response.choices[0].message.content

            st.write(result)
