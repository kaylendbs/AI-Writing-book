import streamlit as st

st.set_page_config(page_title="전자책 생성기", page_icon="📘", layout="centered")

st.title("📘 전자책 생성기")
st.write("주제를 입력하면 전자책 초안을 자동으로 만들어주는 간단한 앱입니다.")

topic = st.text_input("주제를 입력하세요", placeholder="예: AI 자동수익 만드는 방법")

tone = st.selectbox(
    "말투를 선택하세요",
    ["친근한 말투", "전문가형", "마케팅형"]
)

if st.button("전자책 초안 만들기"):
    if topic.strip() == "":
        st.warning("주제를 먼저 입력해주세요!")
    else:
        st.success("전자책 초안이 생성되었습니다.")

        # 제목
        st.header(f"전자책 제목: {topic}")

        # 소개
        st.subheader("1. 소개")
        if tone == "친근한 말투":
            st.write(
                f"이 전자책은 '{topic}'에 관심 있는 초보자도 쉽게 이해할 수 있도록 만든 가이드입니다. "
                "복잡한 설명보다 바로 이해되고 바로 따라할 수 있게 구성했습니다."
            )
        elif tone == "전문가형":
            st.write(
                f"본 전자책은 '{topic}'의 핵심 개념과 실행 방법을 체계적으로 정리한 실전형 가이드입니다. "
                "기초 이해부터 실행 단계까지 순서대로 살펴볼 수 있습니다."
            )
        else:
            st.write(
                f"이 전자책은 '{topic}'을 통해 실제 결과를 만들고 싶은 사람들을 위한 실전 안내서입니다. "
                "불필요한 이론은 줄이고, 바로 실행 가능한 내용 중심으로 구성했습니다."
            )

        # 목차
        st.subheader("2. 목차")
        toc = [
            f"1장. {topic}이 왜 중요한가",
            f"2장. 사람들이 {topic}에서 실패하는 이유",
            f"3장. {topic}을 시작하는 가장 쉬운 방법",
            f"4장. {topic} 실전 실행 단계",
            f"5장. {topic}로 결과를 만드는 팁"
        ]

        for item in toc:
            st.write("- " + item)

        # 본문 초안
        st.subheader("3. 챕터별 초안")

        st.markdown("### 1장. 왜 중요한가")
        st.write(
            f"{topic}은 단순한 정보가 아니라 실제 변화를 만들 수 있는 방법입니다. "
            "많은 사람들이 관심은 있지만 시작하지 못하고, 그 차이 때문에 결과가 갈립니다."
        )

        st.markdown("### 2장. 실패하는 이유")
        st.write(
            f"많은 사람들이 {topic}을 어렵게 생각합니다. "
            "처음부터 완벽하게 하려고 하거나, 너무 많은 정보를 한 번에 보려다가 금방 지치게 됩니다."
        )

        st.markdown("### 3장. 시작하는 가장 쉬운 방법")
        st.write(
            f"{topic}을 시작할 때 가장 좋은 방법은 복잡하게 생각하지 않는 것입니다. "
            "핵심은 작은 단계부터 바로 실행해보는 것입니다."
        )

        st.markdown("### 4장. 실전 실행 단계")
        st.write("STEP 1. 주제를 명확하게 정한다.")
        st.write("STEP 2. 필요한 자료를 간단히 정리한다.")
        st.write("STEP 3. 바로 실행 가능한 작은 행동부터 시작한다.")
        st.write("STEP 4. 실행 후 결과를 보며 수정한다.")

        st.markdown("### 5장. 결과를 만드는 팁")
        st.write(
            "중요한 것은 완벽함이 아니라 지속성입니다. "
            "작게라도 꾸준히 실행하면 훨씬 빠르게 결과를 만들 수 있습니다."
        )
