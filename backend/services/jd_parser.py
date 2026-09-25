"""
Job Description Parser Service
Cleans input job description text and extracts required skills.
"""

from typing import Dict, Any, List
from utils.text_preprocessor import clean_text
from services.skill_extractor import skill_extractor_instance


class JDParser:
    def __init__(self):
        self.skill_extractor = skill_extractor_instance

    def parse(self, raw_text: str) -> Dict[str, Any]:
        """
        Parses Job Description text:
        - Cleans text
        - Extracts skills
        - Returns structured metadata
        """
        cleaned = clean_text(raw_text)
        skills = self.skill_extractor.extract_skills(cleaned)
        skill_names = [s["name"] for s in skills]

        words = cleaned.split()
        
        return {
            "cleaned_text": cleaned,
            "skills": skills,
            "skill_names": skill_names,
            "word_count": len(words),
            "character_count": len(cleaned)
        }


# Singleton instance
jd_parser_instance = JDParser()
