import os

from langchain_community.llms import Ollama
from langchain_community.document_loaders import UnstructuredFileLoader
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains import RetrievalQA

working_dir = os.path.dirname(os.path.abspath(__file__))

#load llm
llm = Ollama(
    model="llama3:instruct",
    temperature=0
)

embedding = HuggingFaceEmbeddings()

#function to take file name and query

def get_answer(file_name,query):
    file_path=f"{working_dir}/{file_name}"
    #loading the documnets
    loader = UnstructuredFileLoader(file_path)
    documents = loader.load()


    #create text chunks
    text_splitter = CharacterTextSplitter(separator="/n",
                                          chunk_size=1000,
                                          chunk_overlap=200)

    text_chunks = text_splitter.split_documents(documents)


    #vector embedding from text chunks
    knowledge_base = FAISS.from_documents(text_chunks,embedding)

    #llm chain
    qa_chain = RetrievalQA.from_chain_type(
        llm,
        retriever =knowledge_base.as_retriever()
    )

    response = qa_chain.invoke({"query":query})

    return response['result']
