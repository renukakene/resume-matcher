"""
Skill Comparison Service
Calculates set-based skill overlap:
- Matching skills (Intersection)
- Missing skills (JD Difference)
- Additional skills (Resume Difference)
- Overlap percentage
"""

from typing import Dict, Any, List, Set


def compare_skills(resume_skills: List[str], jd_skills: List[str]) -> Dict[str, Any]:
    """
    Performs set-based skill comparison between resume skills and job description skills.
    
    Returns:
        Dictionary containing matching_skills, missing_skills, additional_skills,
        counts, and overlap percentage.
    """
    resume_set: Set[str] = set(resume_skills)
    jd_set: Set[str] = set(jd_skills)

    # 1. Matching: present in both
    matching = sorted(list(resume_set.intersection(jd_set)))
    
    # 2. Missing: present in JD but absent in Resume
    missing = sorted(list(jd_set.difference(resume_set)))
    
    # 3. Additional: present in Resume but not requested in JD
    additional = sorted(list(resume_set.difference(jd_set)))

    # Overlap Percentage based on JD required skills
    if len(jd_set) > 0:
        overlap_percentage = round((len(matching) / len(jd_set)) * 100, 1)
    else:
        # If JD specified no skills from the dictionary
        overlap_percentage = 0.0

    return {
        "matching_skills": matching,
        "missing_skills": missing,
        "additional_skills": additional,
        "matching_count": len(matching),
        "missing_count": len(missing),
        "additional_count": len(additional),
        "total_resume_skills": len(resume_set),
        "total_jd_skills": len(jd_set),
        "skill_overlap_percentage": overlap_percentage,
        "explanation": "Skill overlap percentage represents the proportion of detected Job Description skills present in the resume."
    }
