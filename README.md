# 📘 Document_Bassed_Exam_Preparation_Tool

A lightweight Flask application that helps students revise faster:
1️⃣ **Upload** a study PDF,
2️⃣ **Summarize** it into concise key points,
3️⃣ **Generate** multiple-choice quiz questions — **without** using vector databases or RAG.

---

## ✨ Features

* 📄 **PDF ingestion** using PyPDF2 (local-only).
* 🧠 **LangChain-powered** summarization and quiz generation.
* ⚙️ **No external dependencies** like FAISS or Pinecone — fully standalone.
* 💻 **Simple Flask web UI** for easy use and clean workflow.

---

## 🧱 Tech Stack

| Component   | Technology                  |
| ----------- | --------------------------- |
| Backend     | Flask (Python)              |
| AI Logic    | LangChain + OpenAI API      |
| PDF Reading | PyPDF2                      |
| Frontend    | HTML, CSS, Jinja2 Templates |
| Config      | python-dotenv               |
| Testing     | pytest                      |

---

## 📁 Project Structure

```
Document_Bassed_Exam_Preparation_Tool/
├─ app/
│  ├─ __init__.py
│  ├─ routes.py
│  ├─ services/
│  │  ├─ pdf_loader.py          # PDF extraction using PyPDF2
│  │  ├─ summarizer.py          # Summarization logic using LangChain
│  │  └─ quiz_generator.py      # Quiz creation logic using LangChain
│  ├─ templates/
│  │  ├─ base.html              # Shared layout
│  │  ├─ index.html             # Upload + navigation
│  │  ├─ summary.html           # Summary view
│  │  └─ quiz.html              # Quiz question display
│  ├─ static/
│  │  ├─ css/
│  │  │  └─ styles.css          # Basic UI styling
│  │  └─ js/
│  │     └─ app.js              # Small JS interactions
│  └─ utils/
│     └─ text_clean.py          # Text cleanup utilities
├─ instance/
│  └─ uploads/                  # Uploaded PDFs (excluded from Git)
├─ tests/
│  ├─ test_pdf_loader.py
│  ├─ test_summarizer.py
│  └─ test_quiz_generator.py
├─ .env.example                 # Example config file
├─ .gitignore
├─ requirements.txt
├─ run.py                       # Flask entry point
├─ README.md
└─ LICENSE
```

---

## 🚀 Quick Start

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/<your-username>/Document_Bassed_Exam_Preparation_Tool.git
cd Document_Bassed_Exam_Preparation_Tool
```

### 2️⃣ Create Virtual Environment & Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate        # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3️⃣ Configure Environment Variables

Copy `.env.example` → `.env` and set:

```
OPENAI_API_KEY=your_api_key_here
FLASK_ENV=development
SECRET_KEY=your_secret_here
```

### 4️⃣ Run the Application

```bash
python run.py
```

### 5️⃣ Access the App

Open your browser and visit:

```
http://127.0.0.1:5000
```

You can now:

* Upload your **study PDF**
* View the **auto-generated summary**
* Generate **quiz questions** instantly 🎯

---

## 🧪 Running Tests

```bash
pytest
```

---

## ⚠️ Notes

* Designed to run **locally**, no external vector DBs.
* Uses **LangChain prompts** for summarization & question generation.
* Make sure to keep `instance/uploads/` out of version control (auto gitignored).

---

## 🧭 Future Enhancements

* ⏬ Export quiz as CSV/JSON
* 🧩 Adjustable number/difficulty of questions
* 🎯 Interactive scoring and “reveal answer” mode
* 💾 Save quiz sessions for later practice

---