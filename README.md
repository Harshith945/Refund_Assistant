https://huggingface.co/spaces/Harshith945/Refund_Assistant

Click the link to open project

# 💸 AI Refund Policy Assistant

An AI-powered chatbot that helps users understand refund, return, and cancellation policies across different companies using RAG and rule-based logic.

---

## 🚀 Features

- 🔍 Context-based answers using RAG
- 🧠 Rule engine for accurate decisions
- 🏢 Company-based filtering
- 💬 Chat interface with history
- ⚡ Fast responses using Groq LLM

---

## 🧩 Problem Statement

Understanding refund policies is difficult because:
- Policies are long and complex
- Different companies have different rules
- Users waste time searching for relevant information

---

## 💡 Solution

This system:
- Takes user queries
- Retrieves relevant policy data
- Applies business rules
- Returns clear and accurate responses

---

## 🏗️ Tech Stack

- Streamlit – UI  
- LangChain – RAG pipeline  
- Chroma DB – Vector database  
- Groq (LLaMA 3.1) – LLM  
- Python – Backend  

---

## ⚙️ How It Works

1. User enters a query  
2. Intent detection (greeting / refund / generic)  
3. Retrieve relevant documents from DB  
4. Apply category + company validation  
5. Rule engine processes logic  
6. LLM generates final response  

---

## 🧠 Rule Engine

Custom rules handle real-world scenarios:

- 📱 Electronics → refund for defects  
- 👕 Clothing → must be unused  
- 🍔 Food → refund if spoiled/expired  
- 📚 Books → refund for misprints/damage  
- 🏃 Sportswear → hygiene restrictions  
- 🛒 General items → based on condition  

---

## 🏢 Company Filtering

- Users can select a company  
- Prevents irrelevant responses  
- Shows category if query mismatches  

---

## 💻 UI Features

- Chat input with Enter-to-send  
- Sidebar with company selection  
- Chat history display  
- Clear chat option  

---

## 🌐 Deployment

Deployed on Hugging Face Spaces

---

## ⚠️ Challenges

- Handling incorrect AI responses  
- Managing vector DB errors  
- Filtering irrelevant queries  

---

## 🔮 Future Improvements

- Add more categories  
- Improve accuracy  
- Add multilingual support  
- Convert to API  

---

## 📸 Demo

_Add screenshots here_

---

## 🧑‍💻 Author

Your Name
