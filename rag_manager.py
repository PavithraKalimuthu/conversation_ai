import os
import uuid
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

# --------------------------------------------------
# Chroma Client
# --------------------------------------------------

client = chromadb.PersistentClient(path=CHROMA_PATH)

embedding_model = SentenceTransformer(EMBEDDING_MODEL)

splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)


# --------------------------------------------------
# Get User Collection
# --------------------------------------------------

def get_collection(user_id):

    return client.get_or_create_collection(
        name=f"user_{user_id}"
    )


# --------------------------------------------------
# Upload Document
# --------------------------------------------------

def upload_document(user_id, file_path):

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":

        loader = PyPDFLoader(file_path)

    elif extension == ".txt":

        loader = TextLoader(file_path, encoding="utf-8")

    else:

        raise ValueError("Unsupported file type.")

    documents = loader.load()

    text = ""

    for page in documents:

        text += page.page_content + "\n"

    chunks = splitter.split_text(text)

    collection = get_collection(user_id)

    # -----------------------------------------
    # Remove previous uploaded document
    # -----------------------------------------

    existing = collection.get()

    if existing["ids"]:

        collection.delete(
            ids=existing["ids"]
        )

    # -----------------------------------------
    # Store new document
    # -----------------------------------------

    for chunk in chunks:

        embedding = embedding_model.encode(
            chunk
        ).tolist()

        collection.add(

            ids=[str(uuid.uuid4())],

            documents=[chunk],

            embeddings=[embedding]

        )

    print(f"\n✅ Uploaded {len(chunks)} chunks successfully.\n")


# --------------------------------------------------
# Retrieve Context
# --------------------------------------------------

def retrieve_context(user_id, query):

    collection = get_collection(user_id)

    embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(

        query_embeddings=[embedding],

        n_results=3

    )

    print("\n========== RAG RESULTS ==========")
    print(results)
    print("=================================\n")

    documents = results.get("documents")

    if not documents:

        return ""

    docs = documents[0]

    print("\nRetrieved Documents:\n")
    print(docs)

    # Convert retrieved chunks into a single string
    context = "\n\n".join(docs)

    print("\n========== CONTEXT PASSED TO LLM ==========")
    print(context)
    print("==========================================\n")

    return context