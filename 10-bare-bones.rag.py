import streamlit as st
import os
from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.embeddings.google_genai import GoogleGenAIEmbedding
from llama_index.llms.google_genai import GoogleGenAI
from llama_index.core import Settings

load_dotenv()

Settings.llm = GoogleGenAI(model='gemini-2.5-flash')
Settings.embed_model = GoogleGenAIEmbedding(model_name='models/gemini-embedding-001')


@st.cache_resource
def get_handbook_engine():
    documents = SimpleDirectoryReader("./data").load_data()
    index = VectorStoreIndex.from_documents(documents)
    return index.as_query_engine()


st.title("Babson Handbook Chatbot")

if prompt := st.chat_input("Ask about the handbook:"):
    st.write(f"User: {prompt}")

    engine = get_handbook_engine()
    response = engine.query(prompt)

    st.write(f"Assistant: {response}")