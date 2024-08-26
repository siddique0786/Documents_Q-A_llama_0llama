import os
from doc_chat_utility import get_answer
import streamlit as st


working_dir = os.path.dirname(os.path.abspath(__file__))

#page name

st.set_page_config(
    page_title="Chat with Doc",
    layout="centered"
)

#title of the page
st.title("Document Q&A - Llama 3 - Ollama")

#file uploader

uploader_file = st.file_uploader(label="Upload your File", type=["pdf","txt","csv","json"])

#question store ask by user
user_query = st.text_input("Ask your Question")

#creating button for sumit file

if st.button("Run"):
    bytes_data=uploader_file.read()
    file_name = uploader_file.name
    #save the file to the working directory
    file_path = os.path.join(working_dir,file_name)
    with open(file_path,'wb') as f:
        f.write(bytes_data)

    answer = get_answer(file_name,user_query)

    st.success(answer)



