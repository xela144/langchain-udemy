from pathlib import Path
from dotenv import load_dotenv
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import ReadTheDocsLoader
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()


def get_embeddings_instance():
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    return embeddings


def ingest_docs(embedder, rtd_docs_path: Path, index_name: str):
    if not rtd_docs_path.exists():
        raise FileNotFoundError(f"{rtd_docs_path}")
    loader = ReadTheDocsLoader(str(rtd_docs_path))
    raw_documents = loader.load()
    print(f"loaded {len(raw_documents)} documents")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    documents = text_splitter.split_documents(raw_documents)
    for doc in documents:
        new_url = doc.metadata["source"]
        new_url = new_url.replace("langchain-docs", "https:/")
        doc.metadata.update({"source": new_url})

    print(f"Going to add {len(documents)} to Pinecone")
    PineconeVectorStore.from_documents(documents, embedder, index_name=index_name)


if __name__ == "__main__":
    import os

    print("running ingest_docs()")
    embedder = get_embeddings_instance()
    rtd_docs_path = Path("langchain-docs/api.python.langchain.com/en/latest")
    index_name = os.environ["PINECONE_INDEX_NAME"]
    ingest_docs(embedder, rtd_docs_path, index_name)
