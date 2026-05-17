import chromadb
from chromadb.config import Settings
from embeddings import embed_text

class VectorStore:
    def __init__(self):
        self.client = chromadb.Client(Settings(
            chroma_db_impl="duckdb+parquet",
            persist_directory="./chroma_db"
        ))
        
        self.collection = self.client.get_or_create_collection(
            name="documents",
            metadata={"hnsw:space": "cosine"}
        )

    def add_document(self, text: str, metadata: dict):
        embedding = embed_text(text)
        self.collection.add(
            documents=[text],
            embeddings=[embedding],
            metadatas=[metadata],
            ids=[metadata.get("id")]
        )

    def search(self, query: str, top_k: int):
        embedding = embed_text(query)
        results = self.collection.query(
            query_embeddings=[embedding],
            n_results=top_k
        )

        response = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0]
        ):
            response.append({
                "text": doc,
                "metadata": meta,
                "distance": dist
            })

        return response
