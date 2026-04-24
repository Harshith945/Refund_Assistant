import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings

DATA_PATH = "data/refund_policies.json"
PERSIST_DIR = "chroma_db"

def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def prepare_docs(data):
    texts = []
    metadatas = []

    for item in data:
        text = f"""
        Company: {item['company']}
        Category: {item['category']}
        Policy: {item['policy_text']}
        Tags: {', '.join(item.get('tags', []))}
        """

        texts.append(text.strip())
        metadatas.append({
            "company": item["company"],
            "category": item["category"]
        })

    return texts, metadatas

def create_db(texts, metadatas):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    db = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,
        metadatas=metadatas,
        persist_directory=PERSIST_DIR
    )

    db.persist()
    print("✅ DB created with HuggingFace embeddings")

if __name__ == "__main__":
    data = load_data()
    texts, metadatas = prepare_docs(data)
    create_db(texts, metadatas)