# 📚 Automated Book Publication Workflow – The Gates of Morning

A full-stack AI-powered pipeline that scrapes chapters from public domain texts, rewrites them using LLMs, reviews them with AI feedback, allows human-in-the-loop editing, and stores versions in a semantic search database.

---

## 🌟 Project Overview

This project demonstrates an **automated book publication workflow** using AI agents and human collaboration. It supports:

- Web scraping of chapters  
- AI-driven rewriting and reviewing  
- Manual editing with iterative human approval  
- Version control via ChromaDB  
- Semantic retrieval using RL-style embedding search

Built using **Python**, **Playwright**, **ChromaDB**, **SentenceTransformers**, and **HuggingFace Transformers**.

---

## 🧠 Key Capabilities

### ✅ 1. Scraping & Screenshots
- Chapter scraped from:  
  `https://en.wikisource.org/wiki/The_Gates_of_Morning/Book_1/Chapter_1`
- Screenshot saved to `/screenshots/chapter1_page.png`

### ✅ 2. AI Writing & Reviewing
- `ai_writer.py`: Rewrites chapter using `google/flan-t5-base`  
- `ai_reviewer.py`: Analyzes tone, clarity, grammar, engagement  

### ✅ 3. Human-in-the-Loop Workflow
- `human_loop.py` lets users:  
  - Review AI output  
  - Edit using Notepad/nano  
  - Accept, reject, or revise content  
  - Save versions with metadata  

### ✅ 4. Seamless Agentic Integration
- Fully modular flow:  
  `scrape.py` ➝ `ai_writer.py` ➝ `ai_reviewer.py` ➝ `human_loop.py` ➝ `chroma_handler.py`  
- No manual intervention needed between agents  

### ✅ 5. Versioning + RL Semantic Search
- Final versions stored in `/versions/`  
- Indexed in **ChromaDB** with metadata (author, version, tags)  
- `rl_search.py` allows smart retrieval using `SentenceTransformer("all-MiniLM-L6-v2")`

---

## 🛠️ Tech Stack

| Tool                  | Purpose                          |
|-----------------------|----------------------------------|
| Python                | Core language                    |
| Playwright            | Web scraping + screenshots       |
| HuggingFace Transformers | LLM (Flan-T5 for rewriting)     |
| ChromaDB              | Semantic version storage         |
| SentenceTransformers  | RL-style semantic search         |
| Notepad/nano          | Inline manual editing            |

---

## 🗃️ File Structure

softnerve/
│
├── main.py # Orchestrates full workflow
├── scrape.py # Scrapes chapter and saves screenshot
├── ai_writer.py # Rewrites chapter using LLM
├── ai_reviewer.py # Provides feedback on rewritten text
├── human_loop.py # Manual review + edit loop
├── chroma_handler.py # Saves version to ChromaDB
├── rl_search.py # Semantic search on saved content
│
├── /screenshots/ # Saved webpage screenshots
├── /versions/ # Final and draft versions
│
├── config.txt # For API key
├── requirements.txt # Python dependencies
├── README.md # You're reading this!



---

## ✅ Instructions to Run

### 1. Set up environment
bash
pip install -r requirements.txt

### 2.  Run complete pipeline
bash

python main.py

## This will:
Scrape chapter text + screenshot

Rewrite with AI

Review and give feedback

Let user approve/edit

Save to ChromaDB

Allow semantic search of past versions

### 3. Search saved content
bash

python human_loop.py

# Choose option 4 to search past rewritten chapters.

📸 Screenshot Example
Saved to: screenshots/chapter1_page.png

# 🚀 Submission Status
✅ All required tasks are complete and verified:

 Web scraping

 Screenshot capture

 AI rewriting and reviewing

 Human-in-the-loop editing

 Versioning with ChromaDB

 RL-style semantic retrieval

 Modular and agentic design

# ⚠️ Notes

The code is designed for evaluation only.

AI agents are used ethically, and all human edits are logged.

Plagiarism-free. No external copyrighted content used.

📬 Contact
Built for the Soft-Nerve Developer Evaluation Challenge.
Commercial Use: ❌ Not intended.
