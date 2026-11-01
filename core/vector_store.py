# import os 
# from langchain_chroma import Chroma 
# # from langchain_community.embeddings import HuggingFaceEmbeddings
# from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_core.documents import Document
# import ollama
# CHROMA_DIR = "vector_db"
# COLLECTION_NAME = "meeting_transcript"
# EMBEDDING_MODEL  = "nomic-embed-text"

# def get_embeddings():
#     return Ollama.embed(
#         model=EMBEDDING_MODEL,
#         input="Test embedding"
#     )
# # return 


# def build_vector_store(transcipt:str)->Chroma:
#     print("building vector store")
#     spilter=RecursiveCharacterTextSplitter(chunk_size=500,chunk_overlap=50)
#     chunks=spilter.split_text(transcipt)

#     doc=[
#         Document(page_content=chunk ,metadata={"chunk_index":i})
#         for i,chunk in enumerate(chunks)
#     ]
#     embeddings=get_embeddings()
#     vector_store=Chroma.from_documents(
#        documents=docs,
#        embedding=embeddings,
#        collection_name=COLLECTION_NAME,
#        persist_directory=CHROMA_DIR


#     )
# return vector_store


# # for taking the data 

# def load_vector_store() ->Chroma:
#     embeddings = get_embeddings()
#     vector_store = Chroma(
#         collection_name=COLLECTION_NAME,
#         embedding_function= embeddings,
#         persist_directory=CHROMA_DIR
#     )
# return vector_store

# def retriever(vector_store : Chroma, k :int = 4):
#      return vector_store.as_retriever(
#         search_type = 'similarity',
#         search_kwargs = {"k":k}
#     )





    

    
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document

CHROMA_DIR = "vector_db"
COLLECTION_NAME = "meeting_transcript"
EMBEDDING_MODEL = "nomic-embed-text"


# 1. Initialize embedding model
def get_embeddings():
    return OllamaEmbeddings(
        model=EMBEDDING_MODEL
    )


# 2. Build vector store from transcript
def build_vector_store(transcript: str) -> Chroma:
    print("Building vector store...")

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50
    )

    chunks = splitter.split_text(transcript)

    if not chunks:
        raise ValueError("Transcript is empty. Cannot build vector store.")

    docs = [
        Document(
            page_content=chunk,
            metadata={"chunk_index": i}
        )
        for i, chunk in enumerate(chunks)
    ]

    embeddings = get_embeddings()

    vector_store = Chroma.from_documents(
        documents=docs,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR
    )

    print(f"Vector store created with {len(docs)} chunks.")

    return vector_store


# 3. Load existing vector store
def load_vector_store() -> Chroma:
    embeddings = get_embeddings()

    vector_store = Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR
    )

    return vector_store


# 4. Create retriever
def get_retriever(
    vector_store: Chroma,
    k: int = 4
):
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k}
    )
