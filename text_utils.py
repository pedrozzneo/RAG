import re
from typing import List

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def split_sentences(text: str) -> List[str]:
    text = (text or "").strip()
    if not text:
        return []

    text = re.sub(r"\s+", " ", text)
    sentences = re.split(r"(?<=[.!?])\s+", text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_abstract(abstract: str, max_words: int = 120, overlap_sentences: int = 1) -> List[str]:
    sentences = split_sentences(abstract)
    if not sentences:
        return []

    chunks: List[str] = []
    cur: List[str] = []
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
            chunk_docs.append(
                {
                    "id": f"{doc['id']}_c{i+1:02d}",
                    "content": f"Title: {title}\nAbstract (chunk): {ch}".strip(),
                }
            )

    return chunk_docs


def retrieve_best_document(query, documents):
    # Build TF-IDF vectors for the docs
    doc_texts = [d["content"] for d in documents]

    vectorizer = TfidfVectorizer(stop_words="english")
    doc_matrix = vectorizer.fit_transform(doc_texts)

    # Vectorize the query using the same vectorizer
    q_vec = vectorizer.transform([query])

    # Compare query vs every doc with cosine similarity
    sims = cosine_similarity(q_vec, doc_matrix).flatten()

    # Find the best matching document
    best_index = int(sims.argmax())
    best_score = float(sims[best_index])

    print(
        "\n[Retrieval] Best match: "
        + str(documents[best_index]["id"])
        + " score="
        + str(round(best_score, 3))
    )

    # Return the text of the best document (with the id included in the text)
    return "[" + str(documents[best_index]["id"]) + "] " + str(documents[best_index]["content"])


def build_rag_prompt(user_question: str, best_doc_text: str) -> str:
    docs_block = best_doc_text

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

