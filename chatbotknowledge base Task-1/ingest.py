
import hashlib, time, os, json, uuid
from typing import List, Dict
import requests
from bs4 import BeautifulSoup
import feedparser
from embeddings import embed_texts_openai
from vectorstore import add_documents, delete_documents_by_id
from dotenv import load_dotenv

load_dotenv()

SOURCES_FILE = os.getenv('INGESTION_SOURCES_FILE', 'sources.json')
INDEX_FILE = os.getenv('INGESTION_INDEX_FILE', './index.json')
TTL_DAYS = int(os.getenv('PRUNE_TTL_DAYS', '90'))  # default: 90 days

def read_sources():
    with open(SOURCES_FILE, 'r') as f:
        return json.load(f)

def text_chunks(text, chunk_size=800, overlap=200):
    tokens = text.split()
    chunks = []
    i = 0
    while i < len(tokens):
        chunk = ' '.join(tokens[i:i+chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def fetch_rss(url):
    feed = feedparser.parse(url)
    items = []
    for e in feed.entries:
        content = e.get('summary') or e.get('content',[{}])[0].get('value','') or e.get('title','')
        items.append({'id': e.get('id', e.get('link', str(hash(content)))), 'title': e.get('title',''), 'content': content, 'link': e.get('link')})
    return items

def fetch_url(url):
    try:
        r = requests.get(url, timeout=15)
        soup = BeautifulSoup(r.text, 'html.parser')
        paragraphs = [p.get_text().strip() for p in soup.find_all('p') if p.get_text().strip()]
        text = '\n\n'.join(paragraphs)
        return text[:200000]  # limit
    except Exception as e:
        print('fetch_url error', url, e)
        return ''

def hash_text(s):
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def load_index():
    if not os.path.exists(INDEX_FILE):
        return {}
    with open(INDEX_FILE, 'r') as f:
        return json.load(f)

def save_index(idx):
    with open(INDEX_FILE, 'w') as f:
        json.dump(idx, f, indent=2)

def ingest_once():
    sources = read_sources()
    index = load_index()
    seen_ids = set()
    docs_to_add = []
    now_ts = int(time.time())

    # RSS
    for rss in sources.get('rss_feeds', []):
        items = fetch_rss(rss)
        for it in items:
            chunks = text_chunks(it['content'])
            for idx,ch in enumerate(chunks):
                doc_id = hash_text(it.get('link','') + str(idx))
                seen_ids.add(doc_id)
                h = hash_text(ch)
                if doc_id in index and index[doc_id].get('hash') == h:
                    index[doc_id]['last_seen'] = now_ts
                    continue
                docs_to_add.append({'id': doc_id, 'text': ch, 'metadata': {'source': rss, 'title': it.get('title'), 'link': it.get('link'), 'ingested_at': now_ts}})
                index[doc_id] = {'hash': h, 'first_seen': index.get(doc_id, {}).get('first_seen', now_ts), 'last_seen': now_ts, 'source': rss}

    # URLs
    for url in sources.get('urls', []):
        text = fetch_url(url)
        chunks = text_chunks(text)
        for idx,ch in enumerate(chunks):
            doc_id = hash_text(url + str(idx))
            seen_ids.add(doc_id)
            h = hash_text(ch)
            if doc_id in index and index[doc_id].get('hash') == h:
                index[doc_id]['last_seen'] = now_ts
                continue
            docs_to_add.append({'id': doc_id, 'text': ch, 'metadata': {'source': url, 'ingested_at': now_ts}})
            index[doc_id] = {'hash': h, 'first_seen': index.get(doc_id, {}).get('first_seen', now_ts), 'last_seen': now_ts, 'source': url}

    # Detect removed docs (present in index but not seen this run)
    existing_ids = set(index.keys())
    removed = list(existing_ids - seen_ids)
    # Delete if not seen for > 7 days
    to_remove = []
    for rid in removed:
        last = index[rid].get('last_seen', 0)
        if now_ts - last > 7*24*3600:
            to_remove.append(rid)
            del index[rid]

    if to_remove:
        print(f'Removing {len(to_remove)} docs from vector store (not seen recently)')
        delete_documents_by_id(to_remove)

    # Embed and add new/changed docs
    if docs_to_add:
        texts = [d['text'] for d in docs_to_add]
        embeddings = embed_texts_openai(texts)
        for d, emb in zip(docs_to_add, embeddings):
            d['embedding'] = emb
        print(f'Ingesting {len(docs_to_add)} new/changed chunks...')
        add_documents(docs_to_add)
    else:
        print('No new/changed docs to ingest.')

    # Pruning by TTL
    if TTL_DAYS > 0:
        cutoff = now_ts - TTL_DAYS*24*3600
        to_prune = [did for did, meta in list(index.items()) if meta.get('first_seen', now_ts) < cutoff]
        if to_prune:
            print(f'Pruning {len(to_prune)} docs older than {TTL_DAYS} days')
            delete_documents_by_id(to_prune)
            for pid in to_prune:
                index.pop(pid, None)

    save_index(index)

if __name__ == '__main__':
    ingest_once()
