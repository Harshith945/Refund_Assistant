import json
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document

DATA_PATH = "data/refund_policies.json"
PERSIST_DIR = "chroma_db"

# ---------------- LOAD DATA ----------------
def load_data():
    with open(DATA_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

# ---------------- CREATE DOCUMENTS ----------------
def prepare_documents(data):
    docs = []

    for item in data:
        full_text = f"""
Company: {item['company']}
Category: {item['category']}

Policy:
{item['policy_text']}
""".strip()

        docs.append(
            Document(
                page_content=full_text,
                metadata={
                    "company": item["company"],
                    "category": item["category"],
                    "tags": ", ".join(item.get("tags", []))
                }
            )
        )

    return docs

# ---------------- DB CREATION ----------------
def create_db():
    print("🔄 Loading data...")
    data = load_data()

    print("🔄 Preparing documents...")
    documents = prepare_documents(data)

    print("🔄 Splitting into chunks...")

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=50,
        chunk_overlap=25
    )

    split_docs = text_splitter.split_documents(documents)

    print(f"✅ Total chunks created: {len(split_docs)}")

    print("🔄 Initializing embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("🔄 Creating Chroma DB...")
    db = Chroma.from_documents(
        documents=split_docs,
        embedding=embeddings,
        persist_directory=PERSIST_DIR
    )

    db.persist()
    print("✅ Database created successfully!")

# ---------------- RUN ----------------
if __name__ == "__main__":
    create_db()