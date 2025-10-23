
import os, time, json
from typing import List, Dict, Any
from dotenv import load_dotenv
load_dotenv()

VSTORE = os.getenv('VECTOR_STORE', 'chroma')  # 'chroma' (default) or 'pinecone'
PERSIST_DIR = os.getenv("CHROMA_PERSIST_DIRECTORY", "./chroma_db")
INDEX_FILE = os.getenv('INGESTION_INDEX_FILE', './index.json')

def add_documents(docs: List[Dict[str, Any]]):
    """Docs: list of dicts with keys: id, text, metadata, embedding"""
    if VSTORE == 'pinecone':
        try:
            import pinecone, os
            api_key = os.getenv('PINECONE_API_KEY')
            environment = os.getenv('PINECONE_ENVIRONMENT')
            index_name = os.getenv('PINECONE_INDEX_NAME', 'kb-index')
            if not api_key:
                raise RuntimeError('PINECONE_API_KEY not set')
            pinecone.init(api_key=api_key, environment=environment)
            idx = pinecone.Index(index_name)
            to_upsert = []
            for d in docs:
                vec = d.get('embedding')
                if vec is None:
                    continue
                meta = d.get('metadata', {})
                to_upsert.append((d['id'], vec, meta))
            if to_upsert:
                idx.upsert(vectors=to_upsert)
            print(f'Upserted {len(to_upsert)} to Pinecone')
        except Exception as e:
            print('Pinecone add_documents error:', e)
    else:
        try:
            import chromadb
            from chromadb.config import Settings
            client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=PERSIST_DIR))
            COLLECTION_NAME = "kb_chunks"
            if COLLECTION_NAME in [c.name for c in client.list_collections()]:
                col = client.get_collection(COLLECTION_NAME, embedding_function=None)
            else:
                col = client.create_collection(name=COLLECTION_NAME, embedding_function=None)
            ids = [d['id'] for d in docs]
            texts = [d['text'] for d in docs]
            metadatas = [d.get('metadata', {}) for d in docs]
            embeddings = [d.get('embedding') for d in docs]
            if any(v is not None for v in embeddings):
                col.add(ids=ids, documents=texts, metadatas=metadatas, embeddings=embeddings)
            else:
                col.add(ids=ids, documents=texts, metadatas=metadatas)
            client.persist()
            print(f'Added {len(ids)} docs to Chroma')
        except Exception as e:
            print('Chroma add_documents error:', e)

def delete_documents_by_id(ids: List[str]):
    if not ids:
        return
    if VSTORE == 'pinecone':
        try:
            import pinecone, os
            api_key = os.getenv('PINECONE_API_KEY')
            environment = os.getenv('PINECONE_ENVIRONMENT')
            index_name = os.getenv('PINECONE_INDEX_NAME', 'kb-index')
            pinecone.init(api_key=api_key, environment=environment)
            idx = pinecone.Index(index_name)
            idx.delete(ids=ids)
            print(f'Deleted {len(ids)} from Pinecone')
        except Exception as e:
            print('Pinecone delete error:', e)
    else:
        try:
            import chromadb
            from chromadb.config import Settings
            client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=PERSIST_DIR))
            COLLECTION_NAME = "kb_chunks"
            if COLLECTION_NAME in [c.name for c in client.list_collections()]:
                col = client.get_collection(COLLECTION_NAME, embedding_function=None)
                col.delete(ids=ids)
                client.persist()
                print(f'Deleted {len(ids)} from Chroma')
        except Exception as e:
            print('Chroma delete error:', e)

def query_top_k(query_embedding, k=5):
    if VSTORE == 'pinecone':
        try:
            import pinecone, os
            api_key = os.getenv('PINECONE_API_KEY')
            environment = os.getenv('PINECONE_ENVIRONMENT')
            index_name = os.getenv('PINECONE_INDEX_NAME', 'kb-index')
            pinecone.init(api_key=api_key, environment=environment)
            idx = pinecone.Index(index_name)
            res = idx.query(vector=query_embedding, top_k=k, include_metadata=True, include_values=False)
            matches = res.get('matches', [])
            docs = []
            for m in matches:
                docs.append({'id': m['id'], 'score': m.get('score'), 'metadata': m.get('metadata', {})})
            return {'matches': docs}
        except Exception as e:
            print('Pinecone query error:', e)
            return {'matches': []}
    else:
        try:
            import chromadb
            from chromadb.config import Settings
            client = chromadb.Client(Settings(chroma_db_impl="duckdb+parquet", persist_directory=PERSIST_DIR))
            COLLECTION_NAME = "kb_chunks"
            if COLLECTION_NAME in [c.name for c in client.list_collections()]:
                col = client.get_collection(COLLECTION_NAME, embedding_function=None)
                results = col.query(query_embeddings=[query_embedding], n_results=k, include=['documents','metadatas','distances','ids'])
                return results
            else:
                return {'documents': [], 'metadatas': [], 'ids': [], 'distances': []}
        except Exception as e:
            print('Chroma query error:', e)
            return {'documents': [], 'metadatas': [], 'ids': [], 'distances': []}
