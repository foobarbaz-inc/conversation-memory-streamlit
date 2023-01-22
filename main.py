"""Python file to serve as the frontend"""
import streamlit as st
from streamlit_chat import message
from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import ConversationEntityMemory
from langchain.chains.conversation.prompt import ENTITY_MEMORY_CONVERSATION_TEMPLATE
from langchain.llms import OpenAI

# From here down is all the StreamLit UI.
st.set_page_config(page_title="Long-term Memory + Langchain Demo", page_icon=":robot:")
st.header("Long-term Memory + Langchain Demo")

def load_chain(clear_buffer=False):
    """Logic for loading the chain you want to use should go here."""
    llm = OpenAI(temperature=0)
    buffer = st.session_state.get("buffer", [])
    store = st.session_state.get("store", {})
    print("Buffer here: ", buffer)
    print("Store here: ", store)
    if clear_buffer:
        buffer = []
    chain = ConversationChain(
        llm=llm, 
        prompt=ENTITY_MEMORY_CONVERSATION_TEMPLATE,
        memory=ConversationEntityMemory(llm=llm, buffer=buffer, store=store)
    )    
    return chain

def refresh_chain():
    """Refresh the chain variables.."""
    print("refreshing the chain")
    st.session_state["generated"] = []
    st.session_state["past"] = []
    st.session_state["buffer"] = []
    print("chain refreshed")

chain = load_chain()

if "generated" not in st.session_state:
    st.session_state["generated"] = []

if "past" not in st.session_state:
    st.session_state["past"] = []

if "buffer" not in st.session_state:
    st.session_state["buffer"] = chain.memory.buffer
    print("Buffer:", st.session_state["buffer"])

if "store" not in st.session_state:
    st.session_state["store"] = chain.memory.store
    print("Store:", st.session_state["store"])


def get_text():
    input_text = st.text_input("You: ", "Hi!", key="input")
    return input_text


user_input = get_text()

if user_input:
    output = chain.run(input=user_input)
    if not st.session_state["past"]:
        st.session_state["past"] = []
    if not st.session_state["generated"]:
        st.session_state["generated"] = []
    st.session_state["past"].append(user_input)
    st.session_state["generated"].append(output)
    st.session_state["buffer"] = chain.memory.buffer
    st.session_state["store"] = chain.memory.store

if st.session_state["generated"]:

    for i in range(len(st.session_state["generated"]) - 1, -1, -1):
        message(st.session_state["generated"][i], key=str(i))
        message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")

st.sidebar.title("Entities")

st.button("Refresh chat", on_click=refresh_chain)

if chain.memory.store:
    for entity, summary in chain.memory.store.items():
        st.sidebar.write(f"Entity: {entity}, Summary: {summary}")
    #selected_entity = st.sidebar.selectbox("Select an entity", entities)
