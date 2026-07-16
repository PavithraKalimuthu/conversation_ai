import os

import chromadb

from sentence_transformers import SentenceTransformer

from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

from config import (
    CHROMA_PATH,
    EMBEDDING_MODEL
)

client = chromadb.PersistentClient(path=CHROMA_PATH)

embedding_model = SentenceTransformer(
    EMBEDDING_MODEL
)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)


def get_collection(user_id):

    return client.get_or_create_collection(

        name=f"user_{user_id}"

    )


def upload_document(user_id, file_path):

    ext = os.path.splitext(file_path)[1]

    if ext == ".pdf":

        loader = PyPDFLoader(file_path)

    else:

        loader = TextLoader(file_path)

    docs = loader.load()

    text = ""

    for page in docs:

        text += page.page_content

    chunks = splitter.split_text(text)

    collection = get_collection(user_id)

    for i, chunk in enumerate(chunks):

        embedding = embedding_model.encode(
            chunk
        ).tolist()

        collection.add(

            ids=[str(i)],

            documents=[chunk],

            embeddings=[embedding]

        )


def retrieve_context(user_id, query):

    collection = get_collection(user_id)

    embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(

        query_embeddings=[embedding],

        n_results=3

    )

    docs = results["documents"][0]

    return "\n".join(docs)