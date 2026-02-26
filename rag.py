import requests
import os
import re
from urllib.parse import quote
import xml.etree.ElementTree as ET
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def _safe_name(name: str) -> str:
    name = name.strip()
    name = re.sub(r'[<>:"/\\\\|?*]+', "_", name)
    name = re.sub(r"\s+", " ", name).strip()
    return name or "theme"

def fetch_arxiv_documents(theme: str, n: int = 10):
    query = quote(theme.strip())
    url = (
        "https://export.arxiv.org/api/query?"
        f"search_query=all:{query}&start=0&max_results={int(n)}&sortBy=relevance&sortOrder=descending"
    )

    resp = requests.get(url, timeout=30)

    root = ET.fromstring(resp.text)
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
    }

    docs = []
    entries = root.findall("atom:entry", ns)
    for i, entry in enumerate(entries):
        title = (entry.findtext("atom:title", default="", namespaces=ns) or "").strip()
        summary = (entry.findtext("atom:summary", default="", namespaces=ns) or "").strip()

        docs.append({
            "id": f"doc_{i+1:02d}",
            "title": title,
            "abstract": summary,
            "content": f"Title: {title}\nAbstract: {summary}".strip(),
        })

    return docs

def print_documents(documents):
    print("\nDocuments loaded:\n")
    for d in documents:
        title = (d.get("title") or "").strip().replace("\n", " ")
        if len(title) > 90:
            title = title[:87] + "..."
        print(f"- {d['id']}: {title}")
    print()

def save_documents_to_folder(theme: str, documents, base_dir: str = "docs"):
    theme_dir = os.path.join(base_dir, _safe_name(theme))
    os.makedirs(theme_dir, exist_ok=True)

    for d in documents:
        path = os.path.join(theme_dir, f"{d['id']}.txt")
        with open(path, "w", encoding="utf-8") as f:
            f.write(d["content"])

    return theme_dir

def split_sentences(text: str):
    text = (text or "").strip()
    if not text:
        return []

    text = re.sub(r"\s+", " ", text)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]

def chunk_abstract(abstract: str, max_words: int = 120, overlap_sentences: int = 1):
    sentences = split_sentences(abstract)
    if not sentences:
        return []

    chunks = []
    cur = []
    cur_words = 0

    for s in sentences:
        w = len(s.split())

        if cur and (cur_words + w) > max_words:
            chunks.append(" ".join(cur).strip())
            cur = cur[-overlap_sentences:] if overlap_sentences > 0 else []
            cur_words = sum(len(x.split()) for x in cur)

        cur.append(s)
        cur_words += w

    if cur:
        chunks.append(" ".join(cur).strip())

    return chunks

def build_chunk_documents(documents, max_words: int = 120, overlap_sentences: int = 1):
    chunk_docs = []
    for doc in documents:
        title = doc.get("title", "")
        abstract = doc.get("abstract", "")
        chunks = chunk_abstract(abstract, max_words=max_words, overlap_sentences=overlap_sentences)

        for i, ch in enumerate(chunks):
            chunk_docs.append({
                "id": f"{doc['id']}_c{i+1:02d}",
                "content": f"Title: {title}\nAbstract (chunk): {ch}".strip(),
            })

    return chunk_docs

def retrieve_best_document(query, documents):
    # Build TF-IDF vectors for the docs
    doc_texts = []
    for d in documents:
        doc_texts.append(d["content"])

    vectorizer = TfidfVectorizer(stop_words="english")
    doc_matrix = vectorizer.fit_transform(doc_texts)

    # Vectorize the query using the same vectorizer
    q_vec = vectorizer.transform([query])

    # Compare query vs every doc with cosine similarity
    sims = cosine_similarity(q_vec, doc_matrix).flatten()

    # Find the best matching document
    best_index = 0
    best_score = float(sims[0])

    i = 1
    while i < len(sims):
        score = float(sims[i])
        if score > best_score:
            best_score = score
            best_index = i
        i += 1

    print("\n[Retrieval] Best match: " + str(documents[best_index]["id"]) + " score=" + str(round(best_score, 3)))

    # Return the text of the best document (with the id included in the text)
    return "[" + str(documents[best_index]["id"]) + "] " + str(documents[best_index]["content"])

def build_rag_prompt(user_question, best_doc_text):
    docs_block = best_doc_text

    # Write the prompt according to the rules
    prompt = (
        "You are a helpful assistant.\n"
        "TASK: Answer the user's question based only on the text sent to you.\n"
        "Be straightforward and give just info from the text.\n\n"
        "DOCUMENTS:\n"
        + docs_block
        + "\n"
        "USER QUESTION:\n"  
        + user_question
        + "\n"
    )
    return prompt

def ask_ollama(prompt, model="llama3.2:1b"):
    url = "http://localhost:11434/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
    }

    resp = requests.post(url, json=payload, timeout=60)

    if resp.status_code != 200:
        return ""

    data = resp.json()

    if "response" in data:
        return data["response"]
    return ""

def main():
    theme = input("Theme (arXiv search): ").strip()
    papers = 5

    documents = fetch_arxiv_documents(theme=theme, n=papers)
    print(f"Loaded {len(documents)} documents from arXiv.")
    print_documents(documents)
    folder = save_documents_to_folder(theme, documents)
    print(f"Saved .txt files to: {folder}\n")

    chunk_documents = build_chunk_documents(documents, max_words=120, overlap_sentences=1)
    print(f"Built {len(chunk_documents)} meaningful chunks (sentence-based).\n")

    while True:
        user_q = input("Request: ")

        best_doc_text = retrieve_best_document(user_q, chunk_documents)

        prompt = build_rag_prompt(user_q, best_doc_text)

        print("\nWaiting...\n")
        answer = ask_ollama(prompt=prompt, model="llama3.2:1b")

        print("Assistant:", answer)
        print()
main()
