import React, { useRef, useState } from "react";
import { UploadCloud, FileText, X, Briefcase, Sparkles, RotateCcw } from "lucide-react";
import { SAMPLE_JOB_DESCRIPTION, loadSampleResumeFile } from "../services/api";

export default function UploadSection({
  resumeFile,
  setResumeFile,
  jobDescription,
  setJobDescription,
  onAnalyze,
  isLoading,
  onReset
}) {
  const fileInputRef = useRef(null);
  const [isDragOver, setIsDragOver] = useState(false);
  const [demoLoading, setDemoLoading] = useState(false);

  const handleFileChange = (e) => {
    const file = e.target.files?.[0];
    if (file) {
      if (!file.name.toLowerCase().endsWith(".pdf")) {
        alert("Please select a PDF file (.pdf).");
        return;
      }
      setResumeFile(file);
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setIsDragOver(false);
    const file = e.dataTransfer.files?.[0];
    if (file) {
      if (!file.name.toLowerCase().endsWith(".pdf")) {
        alert("Please drop a valid PDF file (.pdf).");
        return;
      }
      setResumeFile(file);
    }
  };

  const handleLoadDemo = async () => {
    setDemoLoading(true);
    try {
      const sampleFile = await loadSampleResumeFile();
      setResumeFile(sampleFile);
      setJobDescription(SAMPLE_JOB_DESCRIPTION);
    } catch (err) {
      alert("Could not load sample data: " + err.message);
    } finally {
      setDemoLoading(false);
    }
  };

  const formatFileSize = (bytes) => {
    if (!bytes) return "0 KB";
    const kb = bytes / 1024;
    if (kb < 1024) return `${kb.toFixed(1)} KB`;
    return `${(kb / 1024).toFixed(2)} MB`;
  };

  const wordCount = jobDescription.trim() ? jobDescription.trim().split(/\s+/).length : 0;
  const canAnalyze = resumeFile && jobDescription.trim().length > 10;

  return (
    <div className="upload-container">
      <div className="inputs-grid">
        {/* Left: Resume Upload Card */}
        <div className="input-card">
          <div className="card-header-row">
            <div className="card-title-group">
              <div className="card-header-icon">
                <FileText size={18} />
              </div>
              <h2>1. Upload Resume</h2>
            </div>
            <span className="dropzone-badge">PDF only</span>
          </div>

          {!resumeFile ? (
            <div
              className={`dropzone ${isDragOver ? "active" : ""}`}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              onClick={() => fileInputRef.current?.click()}
            >
              <UploadCloud className="dropzone-icon" />
              <p className="dropzone-title">Click to upload or drag & drop</p>
              <p className="dropzone-sub">PDF files only (Max file size: 10MB)</p>
              <input
                ref={fileInputRef}
                type="file"
                accept=".pdf"
                style={{ display: "none" }}
                onChange={handleFileChange}
              />
            </div>
          ) : (
            <div className="file-preview">
              <div className="file-info">
                <FileText size={24} className="file-icon" />
                <div className="file-details">
                  <h4>{resumeFile.name}</h4>
                  <p>{formatFileSize(resumeFile.size)} • PDF Document</p>
                </div>
              </div>
              <button
                type="button"
                className="btn-remove"
                title="Remove file"
                onClick={() => {
                  setResumeFile(null);
                  if (fileInputRef.current) fileInputRef.current.value = "";
                }}
              >
                <X size={18} />
              </button>
            </div>
          )}
        </div>

        {/* Right: Job Description Card */}
        <div className="input-card">
          <div className="card-header-row">
            <div className="card-title-group">
              <div className="card-header-icon">
                <Briefcase size={18} />
              </div>
              <h2>2. Job Description</h2>
            </div>
            <span className="dropzone-badge">{wordCount} words</span>
          </div>

          <textarea
            className="jd-textarea"
            placeholder="Paste the job description here (e.g. required skills, tech stack, job responsibilities)..."
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />

          <div className="textarea-footer">
            <span>Minimum 15 characters required</span>
            <span>{jobDescription.length} characters</span>
          </div>
        </div>
      </div>

      {/* Action Controls Bar */}
      <div className="actions-bar">
        <button
          className="btn-primary"
          onClick={onAnalyze}
          disabled={!canAnalyze || isLoading}
        >
          <Sparkles size={18} />
          {isLoading ? "Analyzing..." : "Analyze Resume"}
        </button>

        <button
          type="button"
          className="btn-secondary"
          onClick={handleLoadDemo}
          disabled={isLoading || demoLoading}
          title="Load pre-filled sample resume and job description"
        >
          <Sparkles size={16} />
          {demoLoading ? "Loading..." : "Load Demo Sample"}
        </button>

        {(resumeFile || jobDescription) && (
          <button
            type="button"
            className="btn-secondary"
            onClick={onReset}
            disabled={isLoading}
            title="Reset form"
          >
            <RotateCcw size={16} />
            Reset
          </button>
        )}
      </div>
    </div>
  );
}
