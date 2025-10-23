
from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import os, textwrap, time
from vectorstore import query_top_k
from embeddings import embed_texts_openai

load_dotenv()
app = FastAPI()

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-4o-mini')  # change as needed

class Query(BaseModel):
    q: str
    k: int = 5

def build_prompt(query, retrieved_docs):
    context_parts = []
    for i, d in enumerate(retrieved_docs):
        meta = d.get('metadata', {})
        text = d.get('document') or d.get('text') or meta.get('text','')
        # limit context length per doc to 800 chars to avoid huge prompts
        if isinstance(text, str) and len(text) > 800:
            text = text[:800] + '...'
        src = meta.get('source') or meta.get('link') or meta.get('title') or d.get('id','unknown')
        context_parts.append(f"[DOC {i+1}] Source: {src}\n{text}\n")
    context = "\n---\n".join(context_parts)
    prompt = f"You are an assistant that uses the following retrieved documents to answer the user's question.\n\nContext:\n{context}\nUser question: {query}\n\nAnswer concisely and cite the document numbers when relevant (e.g., [DOC 1]). If the answer is unknown, say you don't know."
    return prompt

@app.post('/query')
def query(qobj: Query):
    q = qobj.q
    k = qobj.k
    emb = embed_texts_openai([q])[0]
    results = query_top_k(emb, k=k)
    retrieved = []
    if isinstance(results, dict) and 'documents' in results:
        docs = results.get('documents', [])
        metas = results.get('metadatas', [])
        ids = results.get('ids', [])
        for doc, meta, _id in zip(docs, metas, ids):
            retrieved.append({'id': _id, 'document': doc, 'metadata': meta})
    elif isinstance(results, dict) and 'matches' in results:
        for m in results['matches']:
            retrieved.append({'id': m.get('id'), 'metadata': m.get('metadata', {}), 'score': m.get('score')})
    prompt = build_prompt(q, retrieved[:k])

    try:
        import openai
        openai.api_key = OPENAI_API_KEY
        resp = openai.ChatCompletion.create(model=LLM_MODEL, messages=[{'role':'user','content': prompt}], temperature=0.0, max_tokens=512)
        answer = resp['choices'][0]['message']['content']
    except Exception as e:
        print('LLM call failed:', e)
        answer = 'LLM error or API key missing. Retrieved docs returned instead.'

    return {'answer': answer, 'retrieved': retrieved}
