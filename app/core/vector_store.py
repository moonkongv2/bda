from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter

# 1. Vector DB path (in the current project directory)
PERSIST_DIRECTORY = "./chroma_db"
COLLECTION_NAME = "documents_collection"

# 2. Create embedding model object (using local Ollama)
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://localhost:11434" # local host
)

def save_document_to_vectorstore(doc_id: int, text: str):
    """
    split text in doc to chunk then store into vector DB
    """
    if not text:
        return

    # 1. Chunking
    # chunk_size=1000: split every 1000 character
    # chunk_overlap=200: overlap 200 characters in cotinuous chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = text_splitter.create_documents([text])

    # 2. Add metadata (save doc_id to search only in this document)
    for chunk in chunks:
        chunk.metadata = {"doc_id": str(doc_id)}

    # 3. Store in Vector DB
    # collection_name="doc": concept like table
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIRECTORY,
        collection_name=COLLECTION_NAME,
    )
    # ChromaDB is automatically saved, but still call persist()  to make sure (compatible with old versions)
    # recent versions: auto-save
    print(f"Document {doc_id} saved to Vector DB with {len(chunks)} chunks.")

def delete_document_from_vectorstore(doc_id: int):
    """
    when deleting docs, remove from vector DB"
    """
    vectordb = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )

    # delete data matching doc_id
    # 실제로는 get으로 id 목록을 받아와서 delete 해야 함
    pass


def search_document_contexts(doc_id: int, query: str, k: int = 4) -> list[str]:
    """
    Find top-k relevant chunks in vector DB for a single document.
    """
    vectordb = Chroma(
        persist_directory=PERSIST_DIRECTORY,
        embedding_function=embeddings,
        collection_name=COLLECTION_NAME,
    )
    docs = vectordb.similarity_search(
        query=query,
        k=k,
        filter={"doc_id": str(doc_id)},
    )
    return [doc.page_content for doc in docs if doc.page_content]

