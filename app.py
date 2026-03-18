import streamlit as st

st.title("전자책 생성기")

topic = st.text_input("주제를 입력하세요")

if st.button("만들기"):
    st.write("전자책 주제:", topic)
    st.write("1. 왜 이걸 해야 하는가")
    st.write("2. 사람들이 실패하는 이유")
    st.write("3. 해결 방법")
    st.write("4. 실행 단계")
