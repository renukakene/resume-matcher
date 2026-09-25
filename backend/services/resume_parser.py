"""
Resume Information Extraction Service
Performs rule-based and pattern-based extraction of:
- Name
- Email
- Phone Number
- Education
- Experience
- Projects
- Certifications
- Skills (via SkillExtractor)
"""

import re
from typing import Dict, Any, List, Optional
from utils.text_preprocessor import clean_text
from services.skill_extractor import skill_extractor_instance


class ResumeParser:
    def __init__(self):
        self.skill_extractor = skill_extractor_instance

        # Section keywords mapped to standardized section names
        self.section_patterns = {
            "education": [
                r"\b(?:education|academic background|academics|qualifications|academic credentials)\b"
            ],
            "experience": [
                r"\b(?:work experience|experience|employment history|professional experience|internships|internship experience)\b"
            ],
            "projects": [
                r"\b(?:projects|academic projects|personal projects|key projects|notable projects)\b"
            ],
            "certifications": [
                r"\b(?:certifications|certificates|licenses & certifications|courses & certifications|professional certifications)\b"
            ],
            "skills": [
                r"\b(?:technical skills|skills|core competencies|key skills|technologies)\b"
            ]
        }

    def extract_email(self, text: str) -> str:
        """Extracts candidate email using regex."""
        email_pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"
        match = re.search(email_pattern, text)
        if match:
            return match.group(0).strip()
        return "Not detected"

    def extract_phone(self, text: str) -> str:
        """Extracts phone number using standard international & national formats."""
        # Matches patterns like: +1 (123) 456-7890, +91 9876543210, 123-456-7890, 9876543210
        phone_patterns = [
            r"(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b",
            r"(?:\+?\d{1,3}[-.\s]?)?\b[6-9]\d{9}\b",  # Common 10-digit formats
            r"\b\d{3}[-.\s]\d{3}[-.\s]\d{4}\b"
        ]
        for pattern in phone_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                candidate = match.group(0).strip()
                # Basic check: avoid dates like 2020-2024
                digits_only = re.sub(r"\D", "", candidate)
                if len(digits_only) >= 10:
                    return candidate
        return "Not detected"

    def extract_name(self, text: str) -> str:
        """
        Extracts candidate name from the top lines of the resume.
        Filters out common resume headings, email, phone, links, and addresses.
        """
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        
        # Look in the first 8 lines
        candidate_lines = lines[:8]
        
        ignore_words = {
            "resume", "curriculum", "vitae", "cv", "profile", "contact",
            "email", "phone", "address", "linkedin", "github", "portfolio",
            "summary", "objective", "page", "developer", "engineer"
        }

        for line in candidate_lines:
            line_clean = line.strip()
            # Skip if contains email, phone, or website
            if "@" in line_clean or "http" in line_clean.lower() or "www." in line_clean.lower():
                continue
            
            # Remove bullets or symbols
            clean_line = re.sub(r"[^a-zA-Z\s]", "", line_clean).strip()
            words = clean_line.split()
            
            # Typical human names are 2 to 4 words
            if 2 <= len(words) <= 4:
                # Check that none of the words are in ignore list
                if any(w.lower() in ignore_words for w in words):
                    continue
                # Check that words start with capital letter or whole string is uppercase
                if all(w.istitle() or w.isupper() for w in words):
                    return line_clean

        return "Not detected"

    def _split_into_sections(self, text: str) -> Dict[str, str]:
        """
        Splits resume text into recognized standard sections.
        """
        lines = text.split("\n")
        section_starts: List[Dict[str, Any]] = []

        for idx, line in enumerate(lines):
            line_stripped = line.strip()
            # Section headers are usually short (under 40 chars)
            if not line_stripped or len(line_stripped) > 40:
                continue

            for sec_name, patterns in self.section_patterns.items():
                for pat in patterns:
                    if re.match(rf"^{pat}[:]?$", line_stripped, re.IGNORECASE):
                        section_starts.append({
                            "section": sec_name,
                            "line_idx": idx,
                            "header": line_stripped
                        })
                        break

        # Sort sections by occurrence line
        section_starts.sort(key=lambda s: s["line_idx"])

        extracted_sections: Dict[str, str] = {}
        for i, current in enumerate(section_starts):
            sec_name = current["section"]
            start_line = current["line_idx"] + 1
            if i + 1 < len(section_starts):
                end_line = section_starts[i + 1]["line_idx"]
            else:
                end_line = len(lines)

            content = "\n".join(lines[start_line:end_line]).strip()
            # If section repeated, concatenate
            if sec_name in extracted_sections:
                extracted_sections[sec_name] += "\n" + content
            else:
                extracted_sections[sec_name] = content

        return extracted_sections

    def _clean_section_content(self, raw_content: Optional[str]) -> str:
        """Formats and trims section content, returning 'Not detected' if empty."""
        if not raw_content or not raw_content.strip():
            return "Not detected"
        
        lines = [l.strip() for l in raw_content.split("\n") if l.strip()]
        if not lines:
            return "Not detected"
            
        # Return cleaned text with normalized bullets
        return "\n".join(lines[:15])  # Cap at reasonable length for preview/display

    def parse(self, raw_text: str) -> Dict[str, Any]:
        """
        Main parsing method:
        Takes raw extracted resume text and extracts all components.
        """
        cleaned = clean_text(raw_text)
        sections = self._split_into_sections(cleaned)

        name = self.extract_name(cleaned)
        email = self.extract_email(cleaned)
        phone = self.extract_phone(cleaned)

        education = self._clean_section_content(sections.get("education"))
        experience = self._clean_section_content(sections.get("experience"))
        projects = self._clean_section_content(sections.get("projects"))
        certifications = self._clean_section_content(sections.get("certifications"))

        # Extract skills across entire document
        skills = self.skill_extractor.extract_skills(cleaned)
        skill_names = [s["name"] for s in skills]

        return {
            "name": name,
            "email": email,
            "phone": phone,
            "education": education,
            "experience": experience,
            "projects": projects,
            "certifications": certifications,
            "skills": skills,
            "skill_names": skill_names,
            "raw_text": cleaned,
            "sections_detected": list(sections.keys())
        }


# Singleton instance
resume_parser_instance = ResumeParser()
