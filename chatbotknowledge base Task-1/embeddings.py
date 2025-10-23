
import os
from typing import List
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

def embed_texts_openai(texts: List[str]):
    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        resp = openai.Embedding.create(model='text-embedding-3-small', input=texts)
        return [r['embedding'] for r in resp['data']]
    except Exception as e:
        print('OpenAI embedding error or API key missing:', e)
        # Fallback to sentence-transformers
        try:
            from sentence_transformers import SentenceTransformer
            model = SentenceTransformer('all-MiniLM-L6-v2')
            emb = model.encode(texts, show_progress_bar=False)
            # convert numpy arrays to lists if needed
            return [e.tolist() if hasattr(e, 'tolist') else e for e in emb]
        except Exception as e2:
            print('SentenceTransformer fallback failed:', e2)
            return [None for _ in texts]
