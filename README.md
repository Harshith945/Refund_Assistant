https://huggingface.co/spaces/Harshith945/Refund_Assistant

Click the link to open project

.

🎤 1. Introduction

“Hello everyone,
Today I’m presenting my project — AI Refund Policy Assistant.

This is a smart chatbot that helps users understand refund, return, and cancellation policies of different companies using AI and rule-based logic.”

🎯 2. Problem Statement

“Many users face confusion while checking refund policies because:

Policies are long and complex
Different companies have different rules
It takes time to find relevant information

So, I built a system that gives instant, clear answers based on company policies.”

💡 3. Solution Overview

“My solution is an AI-powered assistant that:

Takes user queries
Retrieves relevant policy data
Applies business rules
Generates accurate responses

It ensures users get clear and correct refund information quickly.”

🏗️ 4. Tech Stack

“I used the following technologies:

Streamlit – for building the web interface
LangChain – for managing LLM and retrieval pipeline
Chroma – to store and search policy documents
Groq (LLaMA 3.1 model) – for fast AI responses
Python – core backend logic”
⚙️ 5. System Architecture

“My system works in the following steps:

User enters a query
Query is checked for intent (greeting, generic, refund-related)
Relevant documents are retrieved from vector database
Category and company are validated
Rule engine applies business logic
If needed, LLM generates final response

This combination improves both accuracy and reliability.”

🧠 6. Key Features
AI-based context-aware responses (RAG)
Rule engine for different product categories
Company filtering for specific answers
Intent detection (greeting, generic, refund)
Chat history and UI controls
Handles categories like:
Electronics
Clothing
Food
Books
Sportswear
General items
🔍 7. Rule Engine (Important Highlight)

“One of the key parts is the rule engine.

Instead of relying only on AI:

I added logic for real-world scenarios
Example:
Damaged electronics → eligible for refund
Used clothing → not eligible
Spoiled food → eligible

This reduces incorrect AI responses.”
