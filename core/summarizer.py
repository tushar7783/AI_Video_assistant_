from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate # we acn use  message as well
from langchain_core.output_parsers import StrOutputParser  
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from langchain_ollama import ChatOllama

import os 


# def get_llm():
#     return ChatMistralAI(model="mistral-small-latest",mistral_api_key=os.getenv("MISTRAL_API_KEY"),temperature=0.1)

# def split_transcript(transcript:str)->list:
#     spilter=RecursiveCharacterTextSplitter(
#         # chunk_size=
#          chunk_size = 3000,
#         chunk_overlap = 200
#     )
#     return spilter.split_text(transcript)

# def summarize(transcript:str)->str:
#     llm =get_llm()
#     # created prompt
#     map_prompt=ChatPromptTemplate.from_messages(
#         [
#         ("system", "Summarize this portion of a meeting transcript concisely."),
#         ("human", "{text}"),
#     ]
#     )
#     map_chain=map_prompt|llm|StrOutputParser() # pipe operatorst we pass text and it will go to prompt then to llm then output parserirdt 
#     chunks=split_transcript(transcript)
#     # this will store the all chunks summary usinh map_chain
#     chunk_summaries=[map_chain.invoke({"text":chunk}) for chunk in chunks]
#     combined = "\n\n".join(chunk_summaries)
    
#     # summary will be overlap due to 200
#     combined_prompt = ChatPromptTemplate.from_messages(
#         [
#         (
#             "system",
#             "You are an expert meeting summarizer. Combine these partial summaries "
#             "into one final professional meeting summary in bullet points.",
#         ),
#         ("human", "{text}"),
#     ]
#     )

#     combined_chain = (
#         RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) | combined_prompt | llm | StrOutputParser()
#     )

#     return combined_chain.invoke(combined)


# def generate_title(transcipt:str)->str:
#     llm = get_llm()

    

#     title_chain = (
#         RunnablePassthrough() | RunnableLambda(lambda x:{"text":x}) | 
#         ChatPromptTemplate.from_messages([
#              (
#                 "system",
#                 "Based on the meeting transcript, generate a short professional meeting title "
#                 "(max 8 words). Only return the title, nothing else.",
#             ),
#             ("human", "{text}"),
#         ])
#         | llm
#         |StrOutputParser()
#     )

#     return title_chain.invoke(transcipt[:2000])





# ------------------------------------------------
# 1. Initialize Ollama LLM
# ------------------------------------------------

def get_llm():
    llm = ChatOllama(
        model="gemma3:1b",
        temperature=0.2
    )
    return llm


# ------------------------------------------------
# 2. Split transcript into chunks
# ------------------------------------------------

def split_transcript(transcript:str)->list:
    spilter=RecursiveCharacterTextSplitter(
        # chunk_size=
         chunk_size = 3000,
        chunk_overlap = 200
    )
    return spilter.split_text(transcript)

 

   



# ------------------------------------------------
# 3. Generate Meeting Summary (Map-Reduce)
# ------------------------------------------------

def summarize(transcript: str) -> str:

    llm = get_llm()

    # MAP PROMPT
    map_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Summarize this portion of a meeting transcript concisely. "
            "Preserve important decisions, action items, names and deadlines."
        ),
        ("human", "{text}")
    ])

    # MAP CHAIN
    map_chain = map_prompt | llm | StrOutputParser()

    # Split transcript
    chunks = split_transcript(transcript)

    if not chunks:
        return "spliting not working"

    # Summarize each chunk
    chunk_summaries = [
        map_chain.invoke({"text": chunk})
        for chunk in chunks
    ]

    # Combine partial summaries
    combined = "\n\n".join(chunk_summaries)

    # REDUCE PROMPT
    combined_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are an expert meeting summarizer. "
            "Combine these partial summaries into one final "
            "professional meeting summary in bullet points. "
            "Remove duplicate information. Preserve decisions, "
            "action items, owners and deadlines. Do not invent facts."
        ),
        ("human", "{text}")
    ])

    # REDUCE CHAIN
    combined_chain = (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"text": x})
        | combined_prompt
        | llm
        | StrOutputParser()
    )

    # Generate final summary
    return combined_chain.invoke(combined)


# ------------------------------------------------
# 4. Generate Meeting Title
# ------------------------------------------------

def generate_title(transcript: str) -> str:

    if not transcript.strip():
        return ""

    llm = get_llm()

    title_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Based on the meeting transcript, generate a short "
            "professional meeting title (maximum 8 words). "
            "Only return the title, nothing else."
        ),
        ("human", "{text}")
    ])

    title_chain = (
        RunnablePassthrough()
        | RunnableLambda(lambda x: {"text": x})
        | title_prompt
        | llm
        | StrOutputParser()
    )

    return title_chain.invoke(transcript[:2000]).strip()

