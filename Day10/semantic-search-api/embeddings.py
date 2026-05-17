from sentence_transformers import SentenceTransformer

# Load once for performance
model = SentenceTransformer("all-MiniLM-L6-v2")

def embed_text(text: str):
    embedding = model.encode(text)
    return embedding.tolist()
