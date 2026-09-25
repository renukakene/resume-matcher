import React, { useState, useEffect } from "react";
import Header from "./components/Header";
import UploadSection from "./components/UploadSection";
import SummaryCards from "./components/SummaryCards";
import ResumeInfoCard from "./components/ResumeInfoCard";
import SkillComparisonSection from "./components/SkillComparisonSection";
import { checkBackendHealth, analyzeResume } from "./services/api";
import { AlertCircle, Sparkles } from "lucide-react";

export default function App() {
  const [backendStatus, setBackendStatus] = useState("checking");
  const [resumeFile, setResumeFile] = useState(null);
  const [jobDescription, setJobDescription] = useState("");
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);
  const [errorMessage, setErrorMessage] = useState("");

  const loadingMessages = [
    "Reading PDF and extracting text with PyMuPDF...",
    "Cleaning text, normalizing whitespace and tokenizing...",
    "Extracting contact details, sections, and canonical skills...",
    "Parsing Job Description requirements...",
    "Computing skill overlap (Matching, Missing, Additional)..."
  ];

  // Check backend health periodically and on load
  useEffect(() => {
    const checkStatus = async () => {
      const res = await checkBackendHealth();
      setBackendStatus(res.status);
    };
    checkStatus();
    const interval = setInterval(checkStatus, 15000);
    return () => clearInterval(interval);
  }, []);

  // Step cycling for loading animation
  useEffect(() => {
    let timer;
    if (isLoading) {
      timer = setInterval(() => {
        setLoadingStep((prev) => (prev + 1) % loadingMessages.length);
      }, 700);
    }
    return () => clearInterval(timer);
  }, [isLoading]);

  const handleAnalyze = async () => {
    if (!resumeFile) {
      setErrorMessage("Please upload a PDF resume first.");
      return;
    }
    if (!jobDescription.trim() || jobDescription.trim().length < 15) {
      setErrorMessage("Please enter a job description of at least 15 characters.");
      return;
    }

    setErrorMessage("");
    setIsLoading(true);
    setLoadingStep(0);

    try {
      const data = await analyzeResume(resumeFile, jobDescription);
      setResult(data);
      // Smooth scroll to results
      setTimeout(() => {
        const el = document.getElementById("results-dashboard");
        if (el) el.scrollIntoView({ behavior: "smooth" });
      }, 100);
    } catch (err) {
      setErrorMessage(err.message || "Failed to analyze resume. Please check if the backend is running.");
    } finally {
      setIsLoading(false);
    }
  };

  const handleReset = () => {
    setResumeFile(null);
    setJobDescription("");
    setResult(null);
    setErrorMessage("");
  };

  return (
    <div className="app-container">
      {/* Top Navigation */}
      <Header />

      <main className="main-content">
        {/* Hero Section */}
        <section className="hero-section">
          <div className="hero-pill">
            <Sparkles size={14} />
            <span>Skill Matching & Parsing</span>
          </div>
          <h2 className="hero-title">Understand your resume against a job description.</h2>
        </section>

        {/* Error notification if any */}
        {errorMessage && (
          <div className="alert-box alert-error">
            <AlertCircle className="alert-icon" size={18} />
            <div>
              <strong>Analysis Error:</strong> {errorMessage}
            </div>
          </div>
        )}

        {/* Input Cards: PDF Upload + JD Textarea */}
        <UploadSection
          resumeFile={resumeFile}
          setResumeFile={setResumeFile}
          jobDescription={jobDescription}
          setJobDescription={setJobDescription}
          onAnalyze={handleAnalyze}
          isLoading={isLoading}
          onReset={handleReset}
        />

        {/* Loading Spinner with simulated NLP steps */}
        {isLoading && (
          <div className="loading-box">
            <div className="spinner"></div>
            <h3 className="loading-text">Analyzing Documents</h3>
            <p className="loading-sub">{loadingMessages[loadingStep]}</p>
          </div>
        )}

        {/* Results Section */}
        {result && (
          <div id="results-dashboard" className="results-container">
            {/* Top 4 Metric Cards */}
            <SummaryCards result={result} />

            {/* Skill Comparison Breakdown (Matching, Missing, Additional) */}
            <SkillComparisonSection
              skillComparison={result.skill_comparison}
              jdInfo={result.jd_info}
            />

            {/* Extracted Resume Information Card */}
            <div className="content-single-col">
              <ResumeInfoCard resumeInfo={result.resume_info} />
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="app-footer">
        <div className="footer-inner">
          <div>
            <strong>ResumeIQ</strong> — Resume & Job Description Analyzer
          </div>
          <div>
            FastAPI • PyMuPDF • NLTK • React & Vite
          </div>
        </div>
      </footer>
    </div>
  );
}
