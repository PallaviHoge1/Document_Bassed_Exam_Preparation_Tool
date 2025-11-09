#!/bin/bash

# ====================================================
# 📘 Setup Script for Document_Bassed_Exam_Preparation_Tool
# Author: Your Name
# Description: Creates folder structure, base files, and venv
# ====================================================

PROJECT_NAME="Document_Bassed_Exam_Preparation_Tool"

echo "🚀 Setting up project: $PROJECT_NAME ..."

# Create main project directory
mkdir -p $PROJECT_NAME
cd $PROJECT_NAME || exit

# ------------------------------
# Create folder structure
# ------------------------------
mkdir -p app/services
mkdir -p app/templates
mkdir -p app/static/css
mkdir -p app/static/js
mkdir -p app/utils
mkdir -p instance/uploads
mkdir -p tests

# ------------------------------
# Create placeholder files
# ------------------------------
touch app/__init__.py
touch app/routes.py
touch app/services/pdf_loader.py
touch app/services/summarizer.py
touch app/services/quiz_generator.py
touch app/utils/text_clean.py
touch tests/test_pdf_loader.py
touch tests/test_summarizer.py
touch tests/test_quiz_generator.py
touch run.py
touch requirements.txt
touch .env.example
touch .gitignore
touch LICENSE
touch README.md

# ------------------------------
# Write default .gitignore
# ------------------------------
cat <<EOF > .gitignore
# Python
__pycache__/
*.pyc
.venv/
.env

# Flask instance
instance/
!instance/.gitkeep

# OS
.DS_Store

# IDE
.vscode/
.idea/
EOF

# ------------------------------
# Write default .env.example
# ------------------------------
cat <<EOF > .env.example
OPENAI_API_KEY=your_api_key_here
FLASK_ENV=development
SECRET_KEY=change_me
EOF

# ------------------------------
# Write requirements.txt
# ------------------------------
cat <<EOF > requirements.txt
Flask>=3.0.0
PyPDF2>=3.0.0
langchain>=0.2.0
openai>=1.40.0
python-dotenv>=1.0.0
jinja2>=3.1.0
itsdangerous>=2.2.0
click>=8.1.0
werkzeug>=3.0.0
pytest>=8.0.0
EOF

# ------------------------------
# Initialize git repo (optional)
# ------------------------------
git init
echo "✅ Initialized git repository."

# ------------------------------
# Create virtual environment
# ------------------------------
python3 -m venv .venv
echo "✅ Virtual environment created."

# ------------------------------
# Activate and install dependencies
# ------------------------------
source .venv/bin/activate
pip install -r requirements.txt
echo "✅ Dependencies installed."

# ------------------------------
# Completion message
# ------------------------------
echo "🎉 Project setup complete!"
echo "📂 Folder structure created under: $(pwd)"
echo "Next steps:"
echo "1️⃣ Activate your venv: source .venv/bin/activate"
echo "2️⃣ Run the app later with: python run.py"