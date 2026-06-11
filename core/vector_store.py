import os
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from dotenv import load_dotenv

load_dotenv()


CHROMA_DIR="vector_db"


def getEmbeddings():
    return  HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2",huggingfacehub_api_token=os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN"))

def build_vector_store(transcript:str)->Chroma:
    print("buliding vector store")
    
    spliting_text = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)
  
    chuncks=spliting_text.split_text(transcript)

    docs=[
        Document(page_content=chunck,metadata={'chunk_index':i})
        for i,chunck in enumerate(chuncks)
    ]
 

    vector_store= Chroma.from_documents(
        documents=docs,
        embedding=getEmbeddings,
        collection_name="meeting_transcript",
        persist_directory=CHROMA_DIR
    )
    
    return vector_store

def load_vector_store()->Chroma:
    embeddings=getEmbeddings()
    vector_store=Chroma(
        collection_name="meeting_transcript",
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR
    )
    return vector_store


def get_retriever(vector_store:Chroma,k:int=4):
    return vector_store.as_retriever(
        search_type='similarity',
        search_kwargs={"k":k}
    )