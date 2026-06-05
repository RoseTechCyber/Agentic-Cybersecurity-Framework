"""
Example ingestion script: read JSON files from a local folder, write documents to Cosmos DB (emulator),
then upsert embeddings into Chroma (local vector DB).
This is a minimal example for development only. Do NOT put credentials in source.
"""
import os
import json
from typing import List

# Cosmos DB SDK
from azure.cosmos import CosmosClient, PartitionKey

# Chroma DB (python client)
import chromadb
from chromadb.utils import embedding_functions


COSMOS_ENDPOINT = os.environ.get("COSMOS_ENDPOINT", "https://localhost:8081")
COSMOS_KEY = os.environ.get("COSMOS_KEY", "C2y6yDjf5/R+ob0N8A7Cgv30VRg=")  # emulator well-known key
DATABASE_NAME = os.environ.get("COSMOS_DB", "acsf_db")
CONTAINER_NAME = os.environ.get("COSMOS_CONTAINER", "documents")

CHROMA_SERVER = os.environ.get("CHROMA_SERVER", "http://localhost:8000")


def init_cosmos():
    client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
    db = client.create_database_if_not_exists(id=DATABASE_NAME)
    container = db.create_container_if_not_exists(
        id=CONTAINER_NAME, partition_key=PartitionKey(path="/id")
    )
    return container


def init_chroma():
    client = chromadb.HttpClient(host=CHROMA_SERVER)
    return client


def embed_texts(texts: List[str]):
    # Placeholder embedding function; integrate a local LLaMA encoder or OpenAI/other as needed.
    # For dev, we use a trivial embedding (length-based) — replace with real embeddings.
    return [[len(t)] * 8 for t in texts]


def ingest_folder(path: str):
    container = init_cosmos()
    chroma = init_chroma()

    collection = chroma.create_collection(name="acsf_documents", metadata={"source":"ingest_example"})

    for fname in os.listdir(path):
        if not fname.endswith('.json'):
            continue
        with open(os.path.join(path, fname), 'r', encoding='utf-8') as fh:
            doc = json.load(fh)
            doc_id = doc.get('id') or fname
            container.upsert_item({
                'id': doc_id,
                'content': doc.get('content', ''),
                'meta': doc.get('meta', {})
            })
            embeddings = embed_texts([doc.get('content', '')])
            collection.add(ids=[doc_id], metadatas=[doc.get('meta', {})], documents=[doc.get('content', '')], embeddings=embeddings)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--path', default='sample_data', help='Path to JSON documents')
    args = parser.parse_args()
    ingest_folder(args.path)
