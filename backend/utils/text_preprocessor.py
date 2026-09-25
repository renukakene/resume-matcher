"""
Text Preprocessing Utility for NLP Pipeline
Handles text normalization, cleaning, tokenization, and stopword removal.
"""

import re
import string
import nltk
from typing import List

# Ensure stopwords are available with safe fallback
try:
    from nltk.corpus import stopwords
    STOPWORDS = set(stopwords.words("english"))
except Exception:
    STOPWORDS = {
        "a", "about", "above", "after", "again", "against", "all", "am", "an", "and",
        "any", "are", "aren't", "as", "at", "be", "because", "been", "before", "being",
        "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
        "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during",
        "each", "few", "for", "from", "further", "had", "hadn't", "has", "hasn't",
        "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here",
        "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i",
        "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't", "it", "it's",
        "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself",
        "no", "nor", "not", "of", "off", "on", "once", "only", "or", "other", "ought",
        "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
        "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such",
        "than", "that", "that's", "the", "their", "theirs", "them", "themselves",
        "then", "there", "there's", "these", "they", "they'd", "they'll", "they're",
        "they've", "this", "those", "through", "to", "too", "under", "until", "up",
        "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
        "weren't", "what", "what's", "when", "when's", "where", "where's", "which",
        "while", "who", "who's", "whom", "why", "why's", "with", "won't", "would",
        "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours",
        "yourself", "yourselves"
    }

# Try importing WordNetLemmatizer with fallback
try:
    from nltk.stem import WordNetLemmatizer
    LEMMATIZER = WordNetLemmatizer()
except Exception:
    LEMMATIZER = None


def clean_text(text: str) -> str:
    """
    Cleans raw text by normalizing whitespace, standardizing bullets,
    and removing non-printable or corrupt characters.
    Preserves original casing for extraction purposes.
    """
    if not text:
        return ""
    
    # Replace common unicode bullet points and dashes
    text = text.replace("\u2022", " • ").replace("\u2023", " • ").replace("\u25e6", " • ")
    text = text.replace("\u2013", "-").replace("\u2014", "-")
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    
    # Replace non-printable ASCII
    text = "".join(ch for ch in text if ch.isprintable() or ch in ["\n", "\t"])
    
    # Normalize multiple tabs or irregular spaces into a single space (while keeping newlines)
    lines = [re.sub(r"[ \t]+", " ", line).strip() for line in text.split("\n")]
    
    # Filter excessive blank lines (more than 2 consecutive)
    cleaned_lines = []
    blank_count = 0
    for line in lines:
        if not line:
            blank_count += 1
            if blank_count <= 1:
                cleaned_lines.append("")
        else:
            blank_count = 0
            cleaned_lines.append(line)
            
    return "\n".join(cleaned_lines).strip()


def tokenize_words(text: str) -> List[str]:
    """
    Tokenizes text into words while keeping technical terms intact.
    """
    if not text:
        return []
    try:
        tokens = nltk.word_tokenize(text)
    except Exception:
        # Fallback regex tokenizer
        tokens = re.findall(r"\b[\w\+\#\.\-]+\b", text)
    return tokens


def preprocess_for_tfidf(text: str) -> str:
    """
    Prepares text for TF-IDF vectorization:
    - Lowercases text
    - Preserves specific tech tokens (c++, c#, node.js, etc.)
    - Removes punctuation and standard stopwords
    - Lemmatizes where appropriate
    """
    if not text:
        return ""
    
    # Lowercase
    text = text.lower()
    
    # Protect special tokens before punctuation stripping
    text = text.replace("c++", " cplusplus ")
    text = text.replace("c#", " csharp ")
    text = text.replace(".net", " dotnet ")
    text = text.replace("node.js", " nodejs ")
    text = text.replace("react.js", " reactjs ")
    text = text.replace("vue.js", " vuejs ")
    text = text.replace("next.js", " nextjs ")
    
    # Remove standard punctuation
    text = re.sub(r"[^\w\s]", " ", text)
    
    # Tokenize
    words = text.split()
    
    # Filter stopwords and short tokens
    cleaned_words = []
    for word in words:
        if word not in STOPWORDS and len(word) > 1:
            if LEMMATIZER:
                try:
                    word = LEMMATIZER.lemmatize(word)
                except Exception:
                    pass
            cleaned_words.append(word)
            
    return " ".join(cleaned_words)
