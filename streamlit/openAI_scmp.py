import streamlit as st
import time
import os
import openai
import pinecone
from langchain.vectorstores import Pinecone, VectorStore
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA

# ------------ TEMPLATE HEADER START (EDIT ONLY RELEVANT FIELDS) ------------


# def feedback_section():  # Define feedback section content
#     st.session_state.click_status = False

#     # Feedback section
#     with st.form("feedback_form"):
#         feedback = st.radio(
#             "How would you rate this response?", ("👍", "👎"), horizontal=True)
#         comment = st.text_input("Additional comments (optional)")
#         click_feedback = st.form_submit_button(
#             label='Send feedback', on_click=form_callback)


# def form_callback():  # Define feedback callback
#     st.session_state.click_status = True
#     # Do something with the feedback


def response_section():
    st.divider()
    st.subheader("Output")
    # Generate the actual prompt section
    with st.expander("**ACTUAL PROMPT**", False):
        st.write(prompt)
    # Generate the response section with temperature
    with st.expander("**RESPONSE**", True):
        st.info(response)
        st.caption("Temperature: 5.0 (Balanced)")


# Initiate the submit button status
if 'click_status' not in st.session_state:
    st.session_state.click_status = False

# Initiate the response msg button status
if 'response_msg' not in st.session_state:
    st.session_state.response_msg = ""

# Set Streamlit app theme
st.set_page_config(page_title="LaunchPad Prototype",
                   page_icon="images/scmp2.png", layout="centered")  # EDIT PAGE TITLE

# Display logo image
#launchpad_icon = "images/scmp2.png"
#st.image(launchpad_icon, width=100)

# Set up app title
st.title("China-US Relations Generative QnA")  # EDIT TITLE

# Display disclaimer message
#st.warning('**This application is in Alpha version**. You should avoid using it for general fact-finding and information retrieval and must never trust the responses completely.')

# Display information section
with st.expander("**Description**", False):   # EDIT TITLE
    # EDIT DESCRIPTION
    st.write('Simple Gen QnA on China-US Relations, with SCMP scrapped data from June 2022 - May 2023')

st.divider()

# ------------ TEMPLATE HEADER END (EDIT ONLY RELEVANT FIELDS) ------------


# ------------ CONTENT AREA START (ADD CODE AFTER HERE) ------------

# (CAN DELETE) Content example. Always provide tooltip and placeholder example where applicable to guide user.

# initialize connection to Pinecone vectorDB
pinecone.init(
    api_key=st.secrets["PINECONE_API"],
    environment="us-west4-gcp-free"  
)

index_name = 'semantic-search-openai'

index = pinecone.Index(index_name)

embeddings=OpenAIEmbeddings(openai_api_key=st.secrets["OPENAI_API"])

@st.cache_resource # solve pinecone protocol error
def load_pinecone_existing_index():
    vectorstore = Pinecone.from_existing_index(index_name, embeddings)
    return vectorstore
vectorstore=load_pinecone_existing_index()

# define llm
llm = ChatOpenAI(
    openai_api_key=st.secrets["OPENAI_API"],
    model_name='gpt-3.5-turbo',
    temperature=0.0
)

#define qa
qa = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=vectorstore.as_retriever() 
)

prompt = st.text_area("What would you like to know?", help="free-text input",
                      placeholder="Who is the CEO of Tiktok?")

if st.button("Submit"):
    if prompt != "":  # check that prompt isn't empty
    # encode query as sentence vector
        with st.spinner('Generating response...'):
            response = qa.run(prompt)
            response_section()
            st.session_state.response_msg = response
            feedback_section()
    else:
        st.error("You must input a prompt to get started")


if st.session_state.click_status:
    response_section()
    st.success("Thank you for your feedback!")

# ------------ CONTENT AREA END (ADD CODE BEFORE HERE) ------------


# ------------ TEMPLATE FOOTER START (EDIT ONLY RELEVANT FIELDS) ------------

st.divider()

# Display feedback message
st.info(
    "💬 Help us improve the application by [sharing your feedback with us](http://go.gov.sg/launchpad-gpt-feedback).")

# Hide streamlit footer
hide_streamlit_style = """
                <style>
                footer {display: none;}
                .stAlert {white-space:pre-wrap;}
                .row-widget.stButton {text-align:left;}
                .st-bk,[kind="primary"],[role="alert"],[data-baseweb="textarea"],[data-baseweb="input"] {border-radius: 8px;}
                </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ------------ TEMPLATE FOOTER END (EDIT ONLY RELEVANT FIELDS) ------------