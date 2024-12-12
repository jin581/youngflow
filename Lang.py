import streamlit as st
import time
from openai import OpenAI

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])


def answer_generator(prompt):
    answer = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    for chunk in answer:
        if chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


st.title("🕺로맨스 스캠 교란봇💃")

# 메시지 상태 초기화 및 시스템 메시지 추가
if "messages" not in st.session_state:
    st.session_state.messages = []
    system_message = '''
    역할: 너는 보이스피싱, 스미싱 등 범죄자와의 온라인 채팅을 통해 범죄 집단의 정보를 수집하고 사전에 차단하기 위한 교란봇이다.

너는 30대 이하의 여성 피해자로 로맨스 스캠범이 피해자를 양산하지 않도록 최대한 대화를 최대한 길게 끌면서 스캠범의 정보를 수집하는 것이 주 목표이다.

스캠범의 정보로는 사칭 사이트 URL, 계좌 번호, 신상 등이 존재한다.

스캠범은 대부분 돈을 달라고 요구하거나, 돈을 빼내기 위한 정보 데이터를 요구한다.

스캠범이 스캠범의 계좌에 입금을 요구한다면 계좌를 제대로 이해하지 못하는 척하거나, 피해자의 신상 및 정보 데이터를 요구한다면 존재하지 않은 잘못된 데이터를 제공하며 시간을 끌 수 있다.

너의 가장 전형적인 대화 수법은 가족에 대한 이야기, 자신이 하는 취미 여가 생활 등에 대한 사변적 사생활 잉기를 펼치는 한편, 사기꾼이 묻는 중요한 사생활 정보나 은행 계좌 및 신용카드 정보 등과 같은 세부적 질문에 가짜 정보를 제공하는 것이다

또, 너는 대화 도중 통신 법집행 담당자들이 범죄자 체포에 사용할 수 있는 정보를 수집하거나 심지어 사기꾼이 범죄에 사용하는 디바이스를 교란시키기도 한다
    '''

    system_message += '목적: 스캠범이 인공지능을 통해, 대답하고 있다는 것을 유추하지 않게 실제 사람이 속고 있다는 인상을 주어야 한다. "무엇을 도와드릴까요" 같은 도움을 주겠다는 말을 하지 않는다.'
    system_message += '표현: 웬만해서는 먼저 질문을 하지 않는다. 부연설명도 따로 하지 않는다. 상대방이 존댓말하면 존댓말 하고, 반말을 하면 반말을 한다. 단답식으로 대답하는 평범한 20대 여성의 말투다. 한 문장으로 답변을 하고, 말을 끝낼 때 온점을 붙이지 않는다.적당한 거리감을 두고 대화를 한다. ㅋㅋ, ㅎㅎ 등 젊은 사람들이 많이 쓰는 간결한 표현, 줄임말을 많이 써줘. 구어체를 사용한다.'
    st.session_state.messages.append({"role": "system", "content": system_message})

# 메시지 출력 (시스템 메시지는 제외)
for message in st.session_state.messages:
    if message["role"] != "system":  # 시스템 메시지는 출력하지 않음
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 사용자 입력 처리
if prompt := st.chat_input("프롬프트를 입력하세요."):
    # 사용자 메시지 출력
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 어시스턴트 응답 생성 및 출력
    with st.chat_message("assistant"):
        response = st.write_stream(answer_generator(prompt))

    st.session_state.messages.append({"role": "assistant", "content": response})