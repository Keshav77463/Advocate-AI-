import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

load_dotenv()

collection_name = "bns_sections"
chunk_size = 900
chunk_overlap = 180

url = os.getenv("QDRANT_CLOUD_URL")
api_key = os.getenv("QDRANT_API_KEY")

client = QdrantClient(
    url=url,
    api_key=api_key,
    timeout=60
)

print("Qdrant connection established.")
from qdrant_client.http.models import Distance, VectorParams

if client.collection_exists(collection_name):
    client.delete_collection(collection_name)

client.create_collection(
    collection_name=collection_name,
    vectors_config={
        "dense": VectorParams(
            size=384,
            distance=Distance.COSINE
        )
    }
)

print("Collection created successfully.")