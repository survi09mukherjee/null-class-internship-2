# 🌐 NullClass Internship -2 Tasks  
**Repository:** [null-class-internship-2](https://github.com/survi09mukherjee/null-class-internship-2)  
**Author:** Survi Mukherjee  
**Organization:** NullClass Internship Program  
**Duration:** October 2025  

---

## 🧠 Project Overview

This repository presents the development of an **intelligent, extensible chatbot ecosystem** capable of understanding multiple languages, responding with emotional intelligence, and serving as a domain expert in specialized areas such as **medicine** and **scientific research**.  

The project integrates **Natural Language Processing (NLP)**, **sentiment analysis**, **language detection**, **vector-based knowledge retrieval**, and **Streamlit-based visualization** to create an end-to-end conversational AI framework.

---

## 🚀 Key Features

- Dynamic Knowledge Base Expansion using Vector Databases  
- Multimodal Chat Support (Text + Images)  
- Medical Domain Q&A Chatbot (MedQuAD Dataset)  
- Scientific Domain Expert Chatbot (arXiv Dataset)  
- Sentiment-Aware Conversational Intelligence  
- Multilingual and Culturally Adaptive Chat Interface  

---

## 📁 Repository Structure


**Explanation:**

- `main_chatbot.py` → Core chatbot engine handling conversation flow.  
- `multilingual_chatbot.py` → Language detection and translation support.  
- `sentiment_module.py` → Sentiment analysis and adaptive response module.  
- `vector_update.py` → Periodic knowledge base updater using vector embeddings.  
- `medical_chatbot.py` → Specialized Q&A system for medical queries (MedQuAD).  
- `research_chatbot.py` → Domain expert chatbot for arXiv papers.  
- `app.py` → Streamlit front-end integrating all chatbot modules.  
- `requirements.txt` → Python dependencies for the project.  
- `README.md` → This documentation file.




---

## 🧩 Internship Tasks and Implementation Details

### **Task 1: Dynamic Knowledge Base Expansion**
**Goal:** Implement a system to periodically update the vector database with new information from selected sources.  
**Implementation:**
- Used a **sentence-transformer model** (`all-MiniLM-L6-v2`) for text embedding.  
- Stored vectors in a **FAISS-based database** for efficient semantic search.  
- Added a `vector_update.py` module that automatically pulls new data from configured text or document sources and reindexes them at regular intervals.  
**Outcome:**  
The chatbot can seamlessly expand its knowledge base without manual retraining, enabling continuous learning.  
**Challenges:**  
Automating clean data ingestion and avoiding redundant embeddings during reindexing.

---

### **Task 2: Multi-Modal Chatbot (Text + Image Understanding)**
**Goal:** Extend the chatbot to handle both text and image modalities.  
**Implementation:**
- Integrated **Google PaLM/Gemini API** for multimodal input processing.  
- Added support for **image captioning**, **visual Q&A**, and **image generation from text prompts**.  
- Responses combine both **visual and textual** context for rich, natural dialogue.  
**Outcome:**  
The chatbot can understand uploaded images, describe them, or generate new images based on user requests.  
**Challenges:**  
Maintaining contextual continuity between image and text exchanges.

---

### **Task 3: Medical Q&A Chatbot (MedQuAD Dataset)**
**Goal:** Create a specialized Q&A chatbot for healthcare queries using the MedQuAD dataset.  
**Implementation:**
- Preprocessed **MedQuAD** question-answer pairs and built a **retrieval-based system** using **TF-IDF + cosine similarity**.  
- Added **entity recognition** for medical terms such as diseases, symptoms, and treatments using **spaCy’s medical NER**.  
- Developed a **Streamlit interface** for users to ask medical questions interactively.  
**Outcome:**  
The chatbot accurately retrieves relevant answers and medical facts from the MedQuAD dataset.  
**Challenges:**  
Handling ambiguous user queries and ensuring medically appropriate responses.

---

### **Task 4: Domain Expert Chatbot (arXiv Dataset)**
**Goal:** Build a chatbot capable of discussing research papers, summarizing content, and explaining complex concepts using the arXiv dataset.  
**Implementation:**
- Extracted metadata and abstracts from the **arXiv Computer Science** subset.  
- Embedded papers using **OpenAI embeddings** and stored them in a **vector database**.  
- Implemented a **retrieval-augmented generation (RAG)** pipeline combining semantic search + open-source LLM (LLaMA or Falcon).  
- Developed a **Streamlit interface** for paper search, summaries, and concept visualization.  
**Outcome:**  
The chatbot answers advanced domain questions, summarizes research papers, and explains topics conversationally.  
**Challenges:**  
Balancing summarization accuracy with inference speed and ensuring contextual continuity across long research queries.

---

### **Task 5: Sentiment-Aware Conversational System**
**Goal:** Integrate sentiment analysis to detect and adapt responses based on user emotions.  
**Implementation:**
- Used a **fine-tuned BERT sentiment classifier** to classify messages as *positive*, *neutral*, or *negative*.  
- Modified the response generator to adjust tone and empathy level dynamically.  
**Outcome:**  
The chatbot’s responses now feel emotionally adaptive, improving user satisfaction and engagement.  
**Challenges:**  
Handling mixed sentiments in long, context-heavy conversations.

---

### **Task 6: Multilingual Chatbot with Automatic Language Detection**
**Goal:** Extend chatbot support to multiple languages with seamless detection and response adaptation.  
**Implementation:**
- Integrated **LangDetect** for automatic language detection.  
- Used **Google Translate API** for real-time translation between English, French, Spanish, and Hindi.  
- Responses are localized using culturally contextual phrases and tone adjustments.  
**Outcome:**  
The chatbot dynamically detects and switches languages, maintaining coherent, context-aware responses.  
**Challenges:**  
Ensuring translation accuracy and retaining contextual nuances across languages.

---

## 🧾 Results Summary

| Task | Description | Implementation Status | Key Outcome |
|------|--------------|-----------------------|--------------|
| 1 | Dynamic Vector DB Update | ✅ Completed | Auto-refreshing knowledge base |
| 2 | Multi-Modal Chatbot | ✅ Completed | Text-image conversational capability |
| 3 | Medical Q&A (MedQuAD) | ✅ Completed | Domain-specific medical query handling |
| 4 | Domain Expert (arXiv) | ✅ Completed | Summarization and paper understanding |
| 5 | Sentiment Analysis | ✅ Completed | Emotion-aware adaptive responses |
| 6 | Multilingual Support | ✅ Completed | Seamless multi-language communication |

---

## 💻 Technologies Used

- **Python**  
- **Streamlit**  
- **FAISS / ChromaDB**  
- **Sentence Transformers**  
- **OpenAI & Google PaLM APIs**  
- **spaCy / NLTK / HuggingFace Transformers**  
- **MedQuAD & arXiv Datasets**  
- **LangDetect, Google Translate API**  

---

## 🧮 Challenges Faced

- Handling real-time multilingual translation without latency.  
- Maintaining coherence in long multimodal conversations.  
- Data cleaning and embedding optimization for large text corpora.  
- Ensuring response factuality in medical and scientific contexts.  

---

## 🏁 Conclusion

This project successfully demonstrates the development of a **comprehensive, intelligent chatbot ecosystem** capable of multi-language, multimodal, and domain-specific conversations with dynamic knowledge expansion and emotional intelligence.

It represents a major step toward creating chatbots that are **contextually aware, adaptive, and continuously evolving** — combining the strengths of NLP, retrieval systems, and user-centered design.

---

🪄 *Developed by Survi Mukherjee under the NullClass Internship Program (2025)*  
📧 **Contact:** survi09mukherjee@gmail.com  
🌐 **GitHub:** [survi09mukherjee](https://github.com/survi09mukherjee)


