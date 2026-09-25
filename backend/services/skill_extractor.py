"""
Skill Extraction Service
Uses a controlled skill dictionary with alias matching and regex pattern boundaries
to reliably detect skills in resume and job description texts.
"""

import os
import json
import re
from typing import List, Dict, Set, Any

DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "skills.json")


class SkillExtractor:
    def __init__(self, dictionary_path: str = DATA_PATH):
        self.dictionary_path = dictionary_path
        self.skills_data: List[Dict[str, Any]] = []
        self.compiled_rules: List[Dict[str, Any]] = []
        self.load_dictionary()

    def load_dictionary(self):
        """Loads and compiles skills and their aliases into regex patterns."""
        if not os.path.exists(self.dictionary_path):
            raise FileNotFoundError(f"Skill dictionary not found at: {self.dictionary_path}")

        with open(self.dictionary_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.skills_data = data.get("skills", [])

        self.compiled_rules = []
        for item in self.skills_data:
            canonical_name = item["name"]
            category = item.get("category", "General")
            aliases = item.get("aliases", [canonical_name.lower()])

            # Also ensure canonical name itself is checked
            all_patterns = set(a.lower().strip() for a in aliases)
            all_patterns.add(canonical_name.lower().strip())

            regex_patterns = []
            for pattern in all_patterns:
                # Special boundary handling for non-alphanumeric trailing/leading chars like C++, C#, .NET
                escaped = re.escape(pattern)
                
                # If skill is single letter 'c', strictly match "c language", "c programming", "c/c++", etc.
                if pattern == "c":
                    regex = re.compile(r"(?i)(?:\b|(?<=\s))c(?=\s*[\/,]\s*(?:c\+\+|cpp|java|python)|\s+programming|\s+language|\b(?!\w))")
                elif pattern in ("c++", "cpp"):
                    regex = re.compile(r"(?i)(?:^|[\s,;/()\[\]])(?:c\+\+|cpp)(?=[\s,;/()\[\].]|$)", re.IGNORECASE)
                elif pattern in ("c#", "csharp"):
                    regex = re.compile(r"(?i)(?:^|[\s,;/()\[\]])(?:c\#|csharp)(?=[\s,;/()\[\].]|$)", re.IGNORECASE)
                elif pattern == "r":
                    regex = re.compile(r"(?i)(?:^|[\s,;/()\[\]])r(?:\s+programming|\s+language)(?=[\s,;/()\[\].]|$)", re.IGNORECASE)
                elif pattern == ".net":
                    regex = re.compile(r"(?i)(?:^|[\s,;/()\[\]])\.net(?=[\s,;/()\[\].]|$)", re.IGNORECASE)
                else:
                    # Standard word boundary matching
                    regex = re.compile(rf"(?i)\b{escaped}\b")

                regex_patterns.append(regex)

            self.compiled_rules.append({
                "name": canonical_name,
                "category": category,
                "patterns": regex_patterns
            })

    def extract_skills(self, text: str) -> List[Dict[str, str]]:
        """
        Extracts all matching skills from the provided text.
        
        Returns:
            List of dictionaries: [{"name": "Python", "category": "Programming Languages"}, ...]
        """
        if not text:
            return []

        # Normalize spaces
        normalized_text = f" {text} "

        detected_skills = []
        seen_names = set()

        for rule in self.compiled_rules:
            skill_name = rule["name"]
            if skill_name in seen_names:
                continue

            matched = False
            for pattern in rule["patterns"]:
                if pattern.search(normalized_text):
                    matched = True
                    break

            if matched:
                detected_skills.append({
                    "name": skill_name,
                    "category": rule["category"]
                })
                seen_names.add(skill_name)

        # Sort alphabetically by skill name
        detected_skills.sort(key=lambda s: s["name"].lower())
        return detected_skills

    def get_skill_names(self, text: str) -> List[str]:
        """Convenience method returning list of unique canonical skill names."""
        extracted = self.extract_skills(text)
        return [item["name"] for item in extracted]


# Singleton instance for simple reuse
skill_extractor_instance = SkillExtractor()
