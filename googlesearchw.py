import streamlit as st
from langchain.utilities import GoogleSearchAPIWrapper
from langchain.utilities import GoogleSerperAPIWrapper
import os

SERPER_API_KEY = os.environ.get("SERPER_API_KEY")
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
GOOGLE_CSE_ID = os.environ.get("GOOGLE_CSE_ID")

izbor = st.radio("Choose method: ", ("Google Search" , "Google Serper"))

if izbor == "Google Search":
    search = GoogleSearchAPIWrapper()
else:
    search = GoogleSerperAPIWrapper()
mysearch = st.text_input("Enter your search query: ")
if mysearch:
    results = search.results(mysearch, num_results=3)
    st.write(results)
