import os
from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams
import pandas as pd
from langchain_community.document_loaders import TextLoader

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
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

sections_meta_path = os.path.join(BASE_DIR, "data", "metadata", "bns_metadata.csv")
sections_folder = os.path.join(BASE_DIR, "data", "Sections")

df_sections = pd.read_csv(sections_meta_path)

bns_documents = []

for i in range(1, 359):
    filepath = os.path.join(sections_folder, f"bns_section_{i}.txt")

    loader = TextLoader(filepath, encoding="utf-8")
    docs = loader.load()

    meta_section = df_sections[df_sections["section"] == i]

    docs[0].metadata["section"] = int(meta_section["section"].values[0])
    docs[0].metadata["title"] = meta_section["title"].values[0]
    docs[0].metadata["description"] = meta_section["description"].values[0]

    bns_documents.append(docs[0])

print("Documents loaded with metadata.")