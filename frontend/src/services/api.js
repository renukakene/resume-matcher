/**
 * API Service for communicating with the FastAPI backend
 */

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000/api";

export async function checkBackendHealth() {
  try {
    const res = await fetch(`${API_BASE_URL}/health`);
    if (!res.ok) throw new Error("Backend not responding");
    return await res.json();
  } catch (err) {
    return { status: "offline", error: err.message };
  }
}

export async function analyzeResume(file, jobDescription) {
  const formData = new FormData();
  formData.append("resume", file);
  formData.append("job_description", jobDescription);

  const res = await fetch(`${API_BASE_URL}/analyze`, {
    method: "POST",
    body: formData,
  });

  if (!res.ok) {
    const errorData = await res.json().catch(() => null);
    const detail = errorData?.detail || `Server error (${res.status})`;
    throw new Error(detail);
  }

  return await res.json();
}

export async function fetchDictionarySkills() {
  const res = await fetch(`${API_BASE_URL}/skills`);
  if (!res.ok) throw new Error("Could not fetch skill dictionary");
  return await res.json();
}

/**
 * Loads the built-in sample resume PDF from public folder
 * for instant one-click demonstration.
 */
export async function loadSampleResumeFile() {
  const response = await fetch("/sample_resume.pdf");
  const blob = await response.blob();
  return new File([blob], "Alex_Johnson_Resume.pdf", { type: "application/pdf" });
}

export const SAMPLE_JOB_DESCRIPTION = `We are looking for a Full Stack Python / React Developer to join our engineering team.

Key Responsibilities & Qualifications:
â€¢ Strong proficiency in Python, JavaScript, and TypeScript
â€¢ Experience building modern web applications using React, HTML5, and CSS3
â€¢ Backend experience with FastAPI or Django and building secure REST APIs
â€¢ Hands-on database design with PostgreSQL or MySQL, plus NoSQL experience with MongoDB
â€¢ Familiarity with containerization using Docker, version control with Git and GitHub
â€¢ Experience with cloud deployments on AWS or Azure
â€¢ Understanding of foundational Data Science, Machine Learning, Scikit-learn, or NLP is a plus
â€¢ Bachelor's degree in Computer Science, IT, or related engineering discipline`;

