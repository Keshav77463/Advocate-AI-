# commit 1: Setup project configuration and Qdrant cloud connection

import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient

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