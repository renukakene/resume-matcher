# ResumeIQ: Resume Parsing and Job Description Skill Matching Using NLP

A lightweight, college-level Natural Language Processing (NLP) mini project designed to extract structured information from PDF resumes and analyze skill alignment against job descriptions.

---

## 1. Problem Statement
Job seekers and students often struggle to identify whether their resumes adequately reflect the specific technical keywords and proficiencies demanded by job descriptions. Meanwhile, manual screening is tedious. This project provides an accessible, interpretable NLP pipeline that parses resumes, extracts candidate details and technical skills using a controlled dictionary, and computes set-based skill overlap without relying on paid external APIs or complex black-box machine learning models.

---

## 2. Project Objectives
- **Automated Ingestion:** Extract clean text directly from multi-page PDF resumes using PyMuPDF (`fitz`).
- **Entity & Section Parsing:** Identify candidate contact details (Name, Email, Phone) and standard resume sections (Education, Experience, Projects, Certifications) via rule-based NLP heuristics.
- **Controlled Skill Extraction:** Match technical skills using a maintainable, JSON-based dictionary supporting common abbreviations and aliases (e.g., *JS → JavaScript*, *NodeJS → Node.js*).
- **Skill Overlap Analysis:** Categorize skills into **Matching**, **Missing**, and **Additional** using set algebra.
- **Skill Overlap Metric:** Calculate percentage alignment between required job description skills and detected resume skills.
- **Modern UI Dashboard:** Provide a clean, interactive React + Vite web dashboard displaying results, key metrics, and an interactive NLP architecture pipeline.

---

## 3. Technology Stack

### Backend
- **Language:** Python 3.10+
- **Framework:** FastAPI
- **Web Server:** Uvicorn
- **PDF Extraction:** PyMuPDF (`fitz`)
- **NLP & Text Processing:** NLTK (`stopwords`, `word_tokenize`, `wordnet`)

### Frontend
- **Framework:** React 18 / 19
- **Build Tool:** Vite
- **Icons:** Lucide React
- **Styling:** Modern Vanilla CSS (responsive design, glassmorphic touches, harmonious typography)

---

## 4. NLP Techniques & Pipeline Workflow

```
         ┌─────────────────────────┐
         │       Resume PDF        │
         └────────────┬────────────┘
                      │  (PyMuPDF / fitz)
                      ▼
         ┌─────────────────────────┐
         │   Raw Text Extraction   │
         └────────────┬────────────┘
                      │
                      ▼
   ┌─────────────────────────────────────┐
   │         Text Preprocessing          │
   │  - Whitespace & bullet cleaning     │
   │  - Tokenization (NLTK)              │
   │  - Stopword filtering               │
   └───────────────┬─────────────────────┘
                   │
         ┌─────────┴─────────┐
         ▼                   ▼
┌──────────────────┐ ┌───────────────────────────┐
│ Section & Entity │ │ Controlled Skill Matching │
│   Extraction     │ │  (Regex + Dictionary)    │
└──────────────────┘ └─────────────┬─────────────┘
                                   │
                                   ▼
             ┌───────────────────────────────────────────┐
             │            Set-Based Comparison           │
             │  - Matching Skills (Intersection)         │
             │  - Missing Skills (JD Difference)         │
             │  - Additional Skills (Resume Difference)  │
             │  - Skill Overlap %                        │
             └───────────────────────────────────────────┘
```

1. **PDF Text Extraction:** Reads raw stream bytes from uploaded PDF documents.
2. **Text Normalization:** Cleans formatting artifacts, unicode bullets, and consecutive blank lines.
3. **Information Extraction:** Employs targeted regular expressions and heuristic filters to identify candidate names, emails, phone numbers, and section boundaries.
4. **Skill Dictionary Matching:** Evaluates text against `data/skills.json` with word boundaries (`\b`), ensuring short acronyms (e.g. `C++`, `C`, `R`) are matched accurately without false positives.
5. **Skill Overlap:** Applies mathematical set intersection and differences to generate clear categorizations:
   - **Matching Skills:** Skills present in both the resume and the job description.
   - **Skills Not Detected (Missing):** Skills demanded by the job description that were not detected in the resume.
   - **Additional Skills:** Skills identified in the resume that were not mentioned in the job description.
   - **Skill Overlap Percentage:** Ratio of matched skills to total skills identified in the job description.

---

## 5. Project Directory Structure

```
resume-matcher/
├── backend/
│   ├── main.py                     # FastAPI application endpoints
│   ├── requirements.txt            # Python dependencies
│   ├── test_pipeline.py            # Automated pipeline test script
│   ├── sample_resume.pdf           # Generated sample resume for demo
│   ├── data/
│   │   └── skills.json             # Controlled skill dictionary with categories & aliases
│   ├── services/
│   │   ├── pdf_extractor.py        # PyMuPDF text extraction
│   │   ├── resume_parser.py        # Candidate info & section extractor
│   │   ├── jd_parser.py            # Job description parser
│   │   ├── skill_extractor.py      # Regex dictionary matcher
│   │   └── similarity.py           # Set comparison & skill overlap calculation
│   └── utils/
│       └── text_preprocessor.py    # Text cleaning, tokenization & stopwords
│
├── frontend/
│   ├── public/
│   │   └── sample_resume.pdf       # Accessible sample for 1-click UI demo
│   ├── src/
│   │   ├── components/
│   │   │   ├── Header.jsx          # App header & status badge
│   │   │   ├── UploadSection.jsx   # PDF dropzone & JD input area
│   │   │   ├── SummaryCards.jsx    # Metric summary cards
│   │   │   ├── ResumeInfoCard.jsx  # Extracted candidate profile
│   │   │   ├── SkillComparisonSection.jsx # Matching/Missing/Additional chips
│   │   │   └── PipelineVisualizer.jsx # Visual NLP architecture cards
│   │   ├── services/
│   │   │   └── api.js              # Fetch requests to FastAPI backend
│   │   ├── App.jsx                 # Main application view
│   │   ├── index.css               # Design system & styles
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md
```

---

## 6. How to Run the Project

### Prerequisites
- **Python 3.10+** installed
- **Node.js 18+** & **npm** installed

---

### Step 1: Start the Backend (Terminal 1)

1. Open a terminal and navigate to the backend folder:
   ```bash
   cd C:\Users\Hp\.gemini\antigravity-ide\scratch\resume-matcher\backend
   ```

2. (Optional but recommended) Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Download required NLTK data (run once):
   ```bash
   python -c "import nltk; nltk.download('punkt'); nltk.download('punkt_tab'); nltk.download('stopwords'); nltk.download('wordnet')"
   ```

4. Launch the FastAPI server with Uvicorn:
   ```bash
   python -m uvicorn main:app --host 127.0.0.1 --port 8000 --reload
   ```

- Backend API will be running at: `http://127.0.0.1:8000`
- Interactive API Docs (Swagger): `http://127.0.0.1:8000/docs`

---

### Step 2: Start the Frontend (Terminal 2)

1. Open a **second terminal** and navigate to the frontend folder:
   ```bash
   cd C:\Users\Hp\.gemini\antigravity-ide\scratch\resume-matcher\frontend
   ```

2. (First time only) Install frontend dependencies:
   ```bash
   npm install
   ```

3. Start the Vite development server:
   ```bash
   npm run dev -- --host 127.0.0.1 --port 5173
   ```

4. Open your browser and go to:
   ```
   http://127.0.0.1:5173/
   ```

---

## 7. How to Use the Application

1. **One-Click Demo (Fastest):**
   - Click the **"Load Demo Sample"** button.
   - The application will automatically attach the pre-configured sample resume (`Alex_Johnson_Resume.pdf`) and fill the Job Description box.
   - Click **"Analyze Resume"** to inspect all extracted fields and matching skills.

2. **Custom Resume & Job Description:**
   - Drag and drop your own PDF resume into the upload box.
   - Paste any target job description into the textarea.
   - Click **"Analyze Resume"**.

---

## 8. Limitations & Future Enhancements

### Limitations
- Only processes text-based PDFs (scanned image PDFs without OCR are not supported).
- Skills extraction relies on the curated dictionary (`skills.json`). Skills not in the dictionary will not be matched.

### Future Enhancements
- Integration of spaCy Named Entity Recognition (NER) for deep entity parsing.
- Support for Word documents (`.docx`).
- Tesseract OCR integration for scanned image resumes.
- Database storage (SQLite / PostgreSQL) for historical comparisons.
