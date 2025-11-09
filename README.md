# 📘 Document_Bassed_Exam_Preparation_Tool

**A lightweight AI-powered study assistant** that helps students revise faster —
📄 **Upload a PDF**, 🧠 **Summarize key concepts**, and 🎯 **Generate multiple-choice quiz questions** —
all locally using **Ollama** or other LLMs — *no cloud, no API costs!*

---

## ✨ Features

* 🧾 **PDF ingestion** using PyPDF2 — extracts clean text from any study document.
* 🧠 **Local summarization** powered by Ollama (works offline).
* 🎯 **Automatic quiz generation** with multiple-choice questions (MCQs).
* 💻 **Simple Flask web interface** — upload → summarize → quiz in 3 clicks.
* ⚙️ **Extensible backend** — supports Ollama, OpenAI, and Hugging Face models.
* 🛡️ **Lightweight and private** — no vector DBs, no RAG, no external dependencies.

---

## 🧱 Tech Stack

| Component              | Technology Used                                    |
| ---------------------- | -------------------------------------------------- |
| **Frontend**           | HTML, CSS, Jinja2                                  |
| **Backend**            | Python (Flask)                                     |
| **AI Engine**          | Ollama (default), optionally OpenAI / Hugging Face |
| **PDF Processing**     | PyPDF2                                             |
| **Environment Config** | python-dotenv                                      |
| **Testing**            | pytest                                             |

---

## 📂 Project Structure

```
Document_Bassed_Exam_Preparation_Tool/
├─ app/
│  ├─ __init__.py               # Flask app setup
│  ├─ routes.py                 # Main routes (upload, summary, quiz)
│  ├─ services/
│  │  ├─ pdf_loader.py          # PDF extraction logic
│  │  ├─ summarizer.py          # Summarization using LLMs
│  │  └─ quiz_generator.py      # Quiz question generation logic
│  ├─ templates/
│  │  ├─ base.html              # Common layout
│  │  ├─ index.html             # Upload UI
│  │  ├─ summary.html           # Summary page
│  │  └─ quiz.html              # Quiz question interface
│  ├─ static/
│  │  ├─ css/styles.css         # Styling
│  │  └─ js/app.js              # Interactions
│  └─ utils/
│     └─ text_clean.py          # Cleans and normalizes extracted text
├─ instance/
│  └─ uploads/                  # Uploaded PDFs (ignored by Git)
├─ tests/                       # Unit tests
│  ├─ test_pdf_loader.py
│  ├─ test_summarizer.py
│  └─ test_quiz_generator.py
├─ run.py                       # Flask entry point
├─ requirements.txt             # Dependencies
├─ .env.example                 # Example environment variables
├─ .gitignore
├─ setup_project.sh             # Script to auto-create structure
└─ README.md
```

---

## ⚙️ Environment Setup

### 🪶 1️⃣ Create `.env`

Copy `.env.example` → `.env`, then update:

```bash
# For local Ollama (default backend)
LLM_BACKEND=ollama
OLLAMA_MODEL=llama3.2:3b

# Optional (for OpenAI or HF use)
OPENAI_API_KEY=your_key_here
HUGGINGFACE_API_KEY=your_key_here

# Flask config
FLASK_ENV=development
SECRET_KEY=your_secret_here
```

---

## 🚀 Run Locally

### 1️⃣ Clone the repo

```bash
git clone https://github.com/<your-username>/Document_Bassed_Exam_Preparation_Tool.git
cd Document_Bassed_Exam_Preparation_Tool
```

### 2️⃣ Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate       # (Windows: .venv\Scripts\activate)
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Start Flask app

```bash
python run.py
```

Now open your browser at 👉 **[http://127.0.0.1:5000](http://127.0.0.1:5000)**

---

## 💡 Using Ollama (Offline Mode)

### 🔹 Install Ollama

Download and install from → [https://ollama.com/download](https://ollama.com/download)

### 🔹 Pull a local model

Choose a small model (works even on CPU):

```bash
ollama pull llama3.2:3b
```

### 🔹 Start your app

```bash
python run.py
```

Now the AI runs entirely **offline** — no API keys or internet required 🎉

---

## 🧠 How It Works

1. **Upload Document**
   → PDF text is extracted using PyPDF2 and cleaned.

2. **Summarize Content**
   → LLM (Ollama, OpenAI, or HF) condenses key ideas into bullet points.

3. **Generate Quiz Questions**
   → AI creates structured MCQs (4 options, one correct answer).

4. **Review & Practice**
   → Quiz page displays questions; “Reveal Answer” toggles show correct answers.

---

## 🧩 Supported Backends

| Backend          | Requires Key | Works Offline | Notes                                           |
| ---------------- | ------------ | ------------- | ----------------------------------------------- |
| **Ollama**       | ❌ No         | ✅ Yes         | Default and fastest local option                |
| **OpenAI**       | ✅ Yes        | ❌ No          | Use `gpt-4o-mini` etc.                          |
| **Hugging Face** | ✅ (free)     | ❌ No          | Works with `zephyr-7b-beta`, `phi-3-mini`, etc. |

Switch by setting `LLM_BACKEND` in `.env`.

---

## 🧪 Running Tests

```bash
pytest
```

---

## 🛠 Troubleshooting

| Issue                 | Likely Cause                  | Fix                                            |
| --------------------- | ----------------------------- | ---------------------------------------------- |
| `Failed to summarize` | Model not found / no key      | Verify `.env` or Ollama model pulled           |
| `Extra data in JSON`  | Model added text outside JSON | Restart app; the parser now trims invalid text |
| `‘a’ KeyError`        | Quiz options misformatted     | Fixed in latest version (normalizes keys)      |
| Slow response         | Using 7B+ model on CPU        | Use smaller model (`llama3.2:3b`)              |

---

## 🧭 Roadmap (Phase 2 Ideas)

* 🧾 **Export quizzes** as CSV / JSON / PDF
* 🧠 **Adaptive difficulty** (easy/medium/hard)
* 🧍 **Scoring & practice mode**
* ⚙️ **Switch model backend from UI**
* 💾 **Session memory** for previously uploaded documents

---
