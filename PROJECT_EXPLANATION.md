# ResumeIQ: Comprehensive Project Architecture & NLP Guide

This document provides a detailed breakdown for college viva, presentation, and code understanding.

---

## 1. File-by-File Breakdown: Which File Does What?

### 📁 Backend (`/backend`)

| File Path | Purpose & Responsibilities |
| :--- | :--- |
| **`main.py`** | **FastAPI Server & Route Controller.** Defines REST API endpoints (`/api/analyze`, `/api/parse-resume`, `/api/health`, `/api/skills`), handles CORS middleware, validates file types (PDF only), and coordinates the entire processing pipeline. |
| **`utils/text_preprocessor.py`** | **NLP Preprocessing Engine.** Contains helper functions for text cleaning, whitespace normalization, punctuation handling, word tokenization using NLTK, stopword removal, and lemmatization. |
| **`services/pdf_extractor.py`** | **PDF Text Ingestion.** Uses `PyMuPDF` (`fitz`) to extract raw text stream bytes from uploaded multi-page PDF documents. Handles scanned/empty PDF checks and password encryption errors. |
| **`services/resume_parser.py`** | **Information Extraction (IE).** Uses regex and heuristic pattern rules to extract candidate profile details: Name, Email, Phone number, and segments standard sections (Education, Experience, Projects, Certifications). |
| **`services/skill_extractor.py`** | **Controlled Dictionary Matcher.** Loads `skills.json`, compiles regex expressions with word boundaries (`\b`), handles technical aliases (e.g., *NodeJS → Node.js*, *JS → JavaScript*), and safely extracts canonical skills. |
| **`services/jd_parser.py`** | **Job Description Parser.** Cleans raw pasted Job Description text, tokenizes it, and extracts technical skill requirements using the skill extractor service. |
| **`services/similarity.py`** | **Set-Algebra Comparison Service.** Performs set intersection and set differences to calculate **Matching Skills**, **Missing Skills**, **Additional Skills**, and the **Skill Overlap Percentage**. |
| **`data/skills.json`** | **Controlled Skill Knowledge Base.** A structured JSON dictionary containing technical skills categorized by domain (Programming, Frontend, Backend, Database, Cloud, ML/AI) along with their aliases and alternate spellings. |
| **`requirements.txt`** | **Backend Dependencies.** Specifies required Python packages (`fastapi`, `uvicorn`, `pymupdf`, `nltk`, `python-multipart`, etc.). |
| **`Procfile`** | **Deployment Configuration.** Tells cloud hosts like Render how to start the FastAPI server using dynamic ports (`$PORT`). |

---

### 📁 Frontend (`/frontend`)

| File Path | Purpose & Responsibilities |
| :--- | :--- |
| **`src/App.jsx`** | **Main Dashboard View.** Coordinates application state (`resumeFile`, `jobDescription`, `result`, `isLoading`, `errorMessage`), manages loading steps, and renders the UI sections. |
| **`src/services/api.js`** | **API Client.** Communicates with the FastAPI backend using `fetch` and `FormData`. Normalizes URLs and provides error diagnostics for cloud/local connections. |
| **`src/components/Header.jsx`** | **Navigation Header.** Clean branding displaying the application name and subtitle. |
| **`src/components/UploadSection.jsx`** | **Input Controls.** Features an interactive drag-and-drop PDF upload card, file size validation, a Job Description textarea with word/character counter, and sample demo loading. |
| **`src/components/SummaryCards.jsx`** | **Top Metrics Cards.** Displays high-level analysis cards: Resume Document name, Skills Detected count, Matching Skills count, and Skill Overlap percentage. |
| **`src/components/SkillComparisonSection.jsx`** | **3-Way Skill Breakdown.** Visual chips categorizing skills into **Matching Skills** (green), **Missing from Resume** (amber), and **Additional Resume Skills** (blue). |
| **`src/components/ResumeInfoCard.jsx`** | **Candidate Profile Card.** Displays parsed candidate contact details and formatted sections (Education, Experience, Projects, Certifications). Displays *"Not detected"* if a field is missing. |
| **`src/index.css`** | **Design System.** Custom responsive Vanilla CSS styling featuring cards, status pills, modern typography (Inter & Outfit), and soft gradients. |

---

## 2. NLP Concepts Applied & Where They Are in Code

Here are the specific Natural Language Processing (NLP) techniques used in this project:

### 1. Text Ingestion & Stream Decoding
- **Concept:** Converting unstructured binary PDF streams into raw textual character sequences.
- **Where:** `backend/services/pdf_extractor.py` (`extract_text_from_pdf`)
- **How:** PyMuPDF iterates through document page objects (`doc.load_page(n).get_text("text")`), decoding stream text while filtering corrupt bytes.

### 2. Text Normalization & Cleaning
- **Concept:** Removing noise, standardizing encoding artifacts, and converting text into a consistent representation.
- **Where:** `backend/utils/text_preprocessor.py` (`clean_text`)
- **How:** Replaces irregular unicode bullet points (`\u2022`, `\u2023`, `\u25e6`) with standard bullets, normalizes dashes, strips non-printable ASCII characters, and collapses repetitive whitespace/blank lines.

### 3. Word Tokenization
- **Concept:** Breaking a continuous text stream into discrete linguistic units (tokens/words).
- **Where:** `backend/utils/text_preprocessor.py` (`tokenize_words`)
- **How:** Employs NLTK’s `word_tokenize` (based on the Punkt sentence and word tokenizer) with a regex fallback (`[\w\+\#\.\-]+`) that preserves technical symbols (like `C++`, `C#`, `.NET`).

### 4. Stopword Removal
- **Concept:** Filtering out ubiquitous grammatical words (*the*, *is*, *at*, *which*, *on*) that carry minimal domain-specific semantic value.
- **Where:** `backend/utils/text_preprocessor.py` (`preprocess_for_tfidf`, `STOPWORDS`)
- **How:** Compares candidate tokens against NLTK’s English stopword corpus.

### 5. Lemmatization
- **Concept:** Reducing inflected forms of words to their dictionary base form (lemma) using vocabulary and morphological analysis.
- **Where:** `backend/utils/text_preprocessor.py`
- **How:** Uses NLTK's `WordNetLemmatizer` (`LEMMATIZER.lemmatize(word)`).

### 6. Information Extraction (IE) via Regular Expressions & Rule-Based Heuristics
- **Concept:** Identifying specific semantic entities and document boundaries from unstructured text without training expensive statistical models.
- **Where:** `backend/services/resume_parser.py`
- **How:**
  - **Email:** Standard RFC-compliant regex pattern (`r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"`).
  - **Phone Number:** Multi-format phone regular expressions matching international country codes and 10-digit formats.
  - **Candidate Name:** Heuristic search across the top 8 non-empty lines filtering header stopwords, URLs, and identifying 2–4 capitalized title-case words.
  - **Section Parsing:** Regex keyword boundaries for `EDUCATION`, `EXPERIENCE`, `PROJECTS`, `CERTIFICATIONS`, slicing document text between section headers.

### 7. Controlled Lexicon / Dictionary Matching with Alias Normalization
- **Concept:** Named skill entity extraction using a controlled domain dictionary rather than probabilistic guessing, preventing hallucination.
- **Where:** `backend/services/skill_extractor.py` and `backend/data/skills.json`
- **How:**
  - Maps common abbreviations to canonical names (*"JS"* → *"JavaScript"*, *"NodeJS"* → *"Node.js"*, *"DL"* → *"Deep Learning"*).
  - Uses explicit regex word boundaries (`\b{escaped}\b`) with custom boundary lookarounds for single-letter and symbol-based skills (`C++`, `C#`, `C`).

### 8. Set-Algebra Skill Overlap Analysis
- **Concept:** Mathematical set theory comparison between detected document entities.
- **Where:** `backend/services/similarity.py` (`compare_skills`)
- **How:**
  - **Matching Skills:** Set intersection: $\text{Resume} \cap \text{JD}$
  - **Missing Skills:** Set difference: $\text{JD} \setminus \text{Resume}$
  - **Additional Skills:** Set difference: $\text{Resume} \setminus \text{JD}$
  - **Skill Overlap Percentage:** $\frac{|\text{Matching}|}{|\text{JD Skills}|} \times 100\%$

---

## 3. End-to-End Program Flow

```
[User Interface (React + Vite)]
   │
   ├─► 1. User selects a PDF Resume & pastes Job Description text
   │
   ├─► 2. Frontend validates file (.pdf only) & sends multipart/form-data POST request
   │
[FastAPI Backend: POST /api/analyze]
   │
   ├─► 3. services/pdf_extractor.py
   │        └─ Extracts raw text stream across all pages using PyMuPDF (fitz)
   │
   ├─► 4. utils/text_preprocessor.py
   │        └─ Normalizes whitespace, cleans characters, and standardizes lines
   │
   ├─► 5. services/resume_parser.py
   │        ├─ Extracts Contact Info: Name, Email, Phone
   │        ├─ Segments Sections: Education, Experience, Projects, Certifications
   │        └─ Calls skill_extractor.py to identify resume skills
   │
   ├─► 6. services/jd_parser.py
   │        └─ Cleans JD text & calls skill_extractor.py to extract required JD skills
   │
   ├─► 7. services/similarity.py
   │        └─ Computes set intersection & differences (Matching, Missing, Additional, Overlap %)
   │
   ├─► 8. Backend returns structured JSON response
   │
[User Interface (React + Vite)]
   │
   └─► 9. Displays results in interactive dashboard:
            ├─ Top Summary Cards (Filename, Total Skills, Matching Skills, Overlap %)
            ├─ 3-Column Skill Breakdown (Matching, Missing, Additional tags)
            └─ Structured Candidate Profile Card (Education, Experience, Projects, etc.)
```
