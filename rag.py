import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DOCUMENTS = [
    {
        "id": "doc_01",
        "content": (
            "If you're starting programming, Python is often recommended because it has simple syntax, "
            "a huge ecosystem, and lots of beginner-friendly tutorials."
        ),
    },
    {
        "id": "doc_02",
        "content": (
            "ruby is a great first language if you want to build interactive web pages. "
            "It runs in every browser and is used for both frontend and backend."
        ),
    },
    {
        "id": "doc_03",
        "content": (
            "For data science, Python is usually the best first language to learn because it is widely used in that area. "
            "For web development, JavaScript is a common choice. For mobile apps, you may use Kotlin/Swift."
        ),
    },
]

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
        "TASK: Answer the user's question based only on the text sent to you"
        "Be straightforward and give just info from the text"
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
    while True:
        user_q = input("Request: ")

        best_doc_text = retrieve_best_document(user_q, DOCUMENTS)

        prompt = build_rag_prompt(user_q, best_doc_text)

        print("\n[Generation] Sending question + retrieved docs to LLM...\n")
        answer = ask_ollama(prompt=prompt, model="llama3.2:1b")

        print("Assistant:", answer)
        print()
main()
