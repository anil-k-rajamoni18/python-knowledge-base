from fastapi import FastAPI, UploadFile, File
import json
from schema import DocumentAddRequest, QueryRequest, QueryResponse
from vectorstore import VectorStore

app = FastAPI(title="Semantic Search API")

db = VectorStore()

@app.get("/")
def home():
    return {"message": "Semantic Search API Running"}

@app.post("/add_document")
def add_document(req: DocumentAddRequest):
    db.add_document(req.text, req.metadata)
    return {"status": "success", "message": "Document added"}

@app.post("/search", response_model=QueryResponse)
def search(req: QueryRequest):
    results = db.search(req.query, req.top_k)
    return QueryResponse(results=results)

@app.post("/upload_json")
async def upload_json(file: UploadFile = File(...)):
    contents = await file.read()
    data = json.loads(contents.decode("utf-8"))

    added_count = 0

    for item in data:
        text = item.get("text")
        metadata = item.get("metadata", {})
        if "id" not in metadata:
            metadata["id"] = str(added_count + 1)

        db.add_document(text, metadata)
        added_count += 1

    return {
        "status": "success",
        "message": f"{added_count} documents added from JSON file"
    }
