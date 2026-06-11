from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough,RunnableLambda
import os
from dotenv import load_dotenv
load_dotenv()

def get_llm():
    return ChatMistralAI(model = "mistral-small-2506",temperature=0.3)

def split_transcript(transcript:str)->list:
    splitter =RecursiveCharacterTextSplitter(chunk_size=3000, chunk_overlap=200)
    return splitter.split_text(transcript)

def summarize(transcript:str)->str:
    llm=get_llm()
    map_prompt=ChatPromptTemplate.from_messages([
        ("system","Summarize the following transcript in a concise manner, focusing on the key points and main ideas. Avoid unnecessary details and provide a clear overview of the content."),
        ("human","{text}")
    ])
    map_chain=map_prompt| llm |StrOutputParser()

    chunks=split_transcript(transcript)
    chunk_summaries=[map_chain.invoke({"text":chunk}) for chunk in chunks]

    combined="\n\n".join(chunk_summaries)

    combine_propmt=ChatPromptTemplate.from_messages([
        ("system","you are a expert meeting summarizer,combine these partial summaries into a comprehensive overview.into  one final professional metting sumary  in bullet points."),
        ("human","{text}")
    ])

    combine_chain=(
        RunnablePassthrough() | RunnableLambda(lambda x:{"text":x})|combine_propmt | llm | StrOutputParser()
    )
    return combine_chain.invoke(combined)

def generate_title(transcript:str)->str:
    llm=get_llm()
    
    title_chain = (
        RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) | 
        ChatPromptTemplate.from_messages([
             (
                "system",
                "Based on the meeting transcript, generate a short professional meeting title "
                "(max 8 words). Only return the title, nothing else.",
            ),
            ("human", "{text}"),
        ])
        | llm
        |StrOutputParser()
    )

    return title_chain.invoke(transcript[:2000])

