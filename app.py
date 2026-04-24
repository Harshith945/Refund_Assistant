
import streamlit as st
import os
from dotenv import load_dotenv

st.set_page_config(page_title="Refund Assistant", page_icon="💸", layout="wide")

from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate

# ---------------- LOAD ENV ----------------
load_dotenv()

os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ["LANGCHAIN_PROJECT"] = "refund-assistant"

PERSIST_DIR = "chroma_db"

# ---------------- SESSION ----------------
if "history" not in st.session_state:
    st.session_state.history = []

# ---------------- INTENT CHECK ----------------
def is_greeting(q):
    return q.lower().strip() in ["hi", "hello", "hey", "hii", "good morning", "good evening"]

def is_generic(q):
    phrases = ["what is ai", "who are you", "tell me about yourself", "how are you"]
    return any(p in q.lower() for p in phrases)

def is_refund_related(q):
    keywords = ["refund", "return", "cancel", "exchange", "warranty", "policy", "eligible", "money back"]
    return any(k in q.lower() for k in keywords)

def get_query_category(query):
    q = query.lower()

    if any(x in q for x in ["food", "spoiled", "expired"]):
        return "food"
    elif any(x in q for x in ["clothes", "shirt", "jeans"]):
        return "clothing"
    elif any(x in q for x in ["phone", "tv", "electronics", "laptop"]):
        return "electronics"
    elif any(x in q for x in ["subscription", "login", "account", "digital"]):
        return "digital"

    return None
# ---------------- RULE ENGINE ----------------

def digital_rule(query, metadata):
    if metadata.get("category") == "digital":
        if any(x in query.lower() for x in ["defective", "broken", "damaged"]):
            return (
                "⚠️ Digital Product Notice\n\n"
                "No physical defects apply.\n"
                "Only access, billing, or activation issues are eligible."
            )
    return None


def electronics_rule(query, metadata):
    if metadata.get("category") == "electronics" or metadata.get("category") == "home":
        if any(x in query.lower() for x in ["damaged", "broken", "defective"]):
            return (
                "✅ You are eligible for refund.\n\n"
                "Reason: Manufacturing defect detected.\n"
                "We will process refund or replacement."
            )
    return None


def clothing_rule(query, metadata):
    if metadata.get("category") == "clothing":
        if any(x in query.lower() for x in ["damaged", "torn", "used","defective"]):
            return (
                "✅ You are eligible for refund.\n\n"
                "Condition: Item must be unused with tags."
            )
    return None


def food_rule(query, metadata):
    if metadata.get("category") == "food":
        q = query.lower()

        if any(x in q for x in ["spoiled", "expired", "bad", "stale", "contaminated"]):
            return (
                "✅ You are eligible for refund.\n\n"
                "Reason: Food is spoiled/expired and unsafe.\n"
                "Refund or replacement will be processed."
            )

        if any(x in q for x in ["wrong item", "incorrect", "missing"]):
            return (
                "✅ You are eligible for refund or replacement.\n\n"
                "Reason: Order mismatch or missing item."
            )

    return None

def books_rule(query, metadata):
    if metadata.get("category") == "books":
        q = query.lower()

        # Damaged / defective
        if any(x in q for x in ["damaged", "torn", "misprint", "defective", "missing pages"]):
            return (
                "✅ You are eligible for refund or replacement.\n\n"
                "Reason: Book is damaged/defective or has missing content."
            )

        # Wrong book delivered
        if any(x in q for x in ["wrong book", "incorrect", "different book"]):
            return (
                "✅ You are eligible for refund or replacement.\n\n"
                "Reason: Incorrect book delivered."
            )

        # Used / already read
        if any(x in q for x in ["used", "read", "old"]):
            return (
                "❌ Book is not eligible for refund.\n\n"
                "Condition: Books must be unused and in original condition."
            )

    return None

def general_rule(query, metadata):
    if metadata.get("category") == "general":
        q = query.lower()

        # Damaged / defective
        if any(x in q for x in ["damaged", "broken", "defective", "faulty"]):
            return (
                "✅ You are eligible for refund or replacement.\n\n"
                "Reason: Product is damaged or defective."
            )

        # Wrong item delivered
        if any(x in q for x in ["wrong item", "incorrect", "different item"]):
            return (
                "✅ You are eligible for refund or replacement.\n\n"
                "Reason: Incorrect item delivered."
            )

        # Missing items
        if any(x in q for x in ["missing", "not received", "incomplete"]):
            return (
                "✅ You are eligible for refund.\n\n"
                "Reason: Item is missing or order is incomplete."
            )

        # Used items
        if any(x in q for x in ["used", "opened", "worn"]):
            return (
                "❌ Item is not eligible for refund.\n\n"
                "Condition: Product must be unused and in original packaging."
            )

    return None

def sportswear_rule(query, metadata):
    if metadata.get("category") in ["sportswear", "sports"]:
        q = query.lower()

        # Damaged / defective
        if any(x in q for x in ["damaged", "torn", "defective", "broken"]):
            return (
                "✅ You are eligible for refund or replacement.\n\n"
                "Reason: Product is damaged or defective."
            )

        # Wrong item / size
        if any(x in q for x in ["wrong item", "incorrect", "wrong size", "size issue"]):
            return (
                "✅ You are eligible for exchange or refund.\n\n"
                "Reason: Incorrect item or size delivered."
            )

        # Used / worn (important for sportswear)
        if any(x in q for x in ["used", "worn", "washed", "sweated"]):
            return (
                "❌ Not eligible for refund.\n\n"
                "Condition: Sportswear must be unused due to hygiene reasons."
            )

    return None


def apply_rules(query, metadata):
    for rule in [digital_rule, electronics_rule, clothing_rule, food_rule, books_rule, general_rule, sportswear_rule]:
        result = rule(query, metadata)
        if result:
            return result
    return None

# ---------------- LOAD DB ----------------
@st.cache_resource
def load_embeddings():
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )


@st.cache_resource
def load_db():
    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=load_embeddings()
    )

db = load_db()

# ---------------- COMPANY CATEGORY ----------------
def get_company_category(docs):
    if not docs:
        return None
    return docs[0].metadata.get("category")

# ---------------- COMPANY LIST ----------------
try:
    all_data = db.get()
    companies = list(set(
        m.get("company", "Unknown") for m in all_data.get("metadatas", [])
    ))
except:
    companies = ["Unknown"]

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("💸 Refund Assistant")

    selected_company = st.selectbox(
        "🏢 Select Company",
        ["All"] + sorted(companies)
    )

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.history = []
st.markdown("## 💬 Chat History")


# ---------------- RETRIEVER ----------------
if selected_company != "All":
    retriever = db.as_retriever(
        search_kwargs={"k": 3, "filter": {"company": selected_company}}
    )
else:
    retriever = db.as_retriever(search_kwargs={"k": 3})

# ---------------- LLM ----------------
groq_api_key = os.getenv("GROQ_API_KEY")

if not groq_api_key:
    st.error("❌ GROQ_API_KEY not found.")
    st.stop()

llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0,
    groq_api_key=groq_api_key
)

# ---------------- PROMPT ----------------
prompt = PromptTemplate(
    template="""
You are a Refund Policy Assistant.

Rules:
- if user greets you,respond politely
- Answer ONLY from context
- give explanation
- Dont generate hallucinated answers 



Context:
{context}

Question:
{question}
""",
    input_variables=["context", "question"]
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt}
)



# ---------------- UI ----------------
st.title("💸 AI Refund Policy Assistant")

with st.form(key="chat_form", clear_on_submit=True):
    query = st.text_input("Ask your question...", key="input_box")
    send = st.form_submit_button("Send")

# ---------------- RESPONSE FLOW ----------------
# ---------------- RESPONSE FLOW ----------------
if send and query:
    with st.spinner("Thinking... 🤔"):

        docs = retriever.get_relevant_documents(query)
        metadata = docs[0].metadata if docs else {}

        company_category = get_company_category(docs)
        query_category = get_query_category(query)

        response = None   # ✅ ALWAYS initialize

        # 1. Greeting
        if is_greeting(query):
            response = "Hello 👋 How can I help you with refund policies?"

        # 2. Generic
        elif is_generic(query):
            response = "⚠️ I am your Refund Assistant and only handle refund-related queries."

        # 3. COMPANY VALIDATION
        elif selected_company != "All" and query_category and company_category:
            if query_category != company_category:
                response = (
                    f"⚠️ This question is not related to {selected_company}.\n\n"
                    f"This company deals with {company_category} products."
                )

        # 4. MAIN LOGIC (only if response not set yet)
        if response is None:
            rule_response = apply_rules(query, metadata)

            if rule_response:
                response = rule_response

            elif not is_refund_related(query):
                response = (
                    "⚠️ I am a Refund Assistant.\n\n"
                    "Please provide refund-related queries."
                )

            else:
                response = qa_chain.invoke({"query": query})["result"]

        # FINAL SAFETY
        if not response:
            response = "⚠️ No response generated."

        st.session_state.history.append((query, response))
        st.rerun()
# ---------------- CHAT HISTORY ----------------
for q, r in st.session_state.history:
    if not r:
        r = "No response generated."

    st.markdown(
        f"<div style='background:#DCF8C6;padding:10px;border-radius:10px;margin:5px 0'><b>You:</b> {q}</div>",
        unsafe_allow_html=True
    )

    st.markdown(
        f"<div style='background:#F1F0F0;padding:10px;border-radius:10px;margin:5px 0 15px 0'><b>Bot:</b> {r}</div>",
        unsafe_allow_html=True
    )
