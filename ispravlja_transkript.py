# ispravlja transkript

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from langchain.schema.messages import HumanMessage, SystemMessage
import streamlit as st

# Ovo je transkript sa greskama
st.subheader('Ispravlja Transkript sa greskama na srpskom jeziku')
st.caption("Ver.28.10.23")

uploaded_file = st.file_uploader('Transkript', type=['txt'])
ceo_text = " "
if uploaded_file is not None:
    with st.form(key='my_form'):
        submit_button = st.form_submit_button(label='Ispravi transkript')
        if submit_button:
            transkript = uploaded_file.getvalue().decode("utf-8")
            text_splitter = RecursiveCharacterTextSplitter(
                # Set a really small chunk size, just to show.
                chunk_size = 10000,
                chunk_overlap  = 0,
                length_function = len,
                is_separator_regex = False,
            )

            texts = text_splitter.create_documents([transkript])
            chat = ChatOpenAI(temperature=0, model = "gpt-3.5-turbo-16k")
            ceo_text = " "

            with st.spinner('Ispravlja se transkript...'):
                placeholder = st.empty()
                total_texts = len(texts)
                for i, text in enumerate(texts, start=1):
                    with placeholder:
                        st.info(f"Obradjuje se {i} od {total_texts} strana")
                    txt=text.page_content
                    messages = [
                    SystemMessage(content="You are the Serbian language expert. you must fix grammar and spelling errors but otherwise keep the text as is, in the Serbian language."), 
                    HumanMessage(content=txt),
                    ]
                    odgovor = chat.invoke(messages).content
                    ceo_text = ceo_text + " " + odgovor

                # na kraju ih sve slepi u jedan dokument i sacuva ga u fajl
                with placeholder:
                    st.success("Zavrsena obrada transkripta")
    if ceo_text != " ":
        st.download_button(
                "Preuzmite ispravljen transkript", ceo_text, file_name=f"korigovan_{uploaded_file.name}"
            )
            



