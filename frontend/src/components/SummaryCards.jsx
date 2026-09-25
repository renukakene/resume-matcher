import React from "react";
import { FileText, Cpu, CheckCircle2, Percent } from "lucide-react";

export default function SummaryCards({ result }) {
  if (!result) return null;

  const { filename, page_count, skill_comparison } = result;

  const totalResumeSkills = skill_comparison?.total_resume_skills || 0;
  const matchingSkillsCount = skill_comparison?.matching_count || 0;
  const overlapPct = skill_comparison?.skill_overlap_percentage ?? 0;

  return (
    <div className="metrics-grid">
      {/* 1. Resume File Card */}
      <div className="metric-card accent-blue">
        <div className="metric-header">
          <span className="metric-label">Resume Document</span>
          <div className="metric-icon-wrap" style={{ background: "#e0f2fe", color: "#0284c7" }}>
            <FileText size={16} />
          </div>
        </div>
        <div className="metric-val" style={{ fontSize: "1.25rem", wordBreak: "break-word" }}>
          {filename}
        </div>
        <div className="metric-sub">{page_count} page(s) parsed via PyMuPDF</div>
      </div>

      {/* 2. Skills Found */}
      <div className="metric-card accent-purple">
        <div className="metric-header">
          <span className="metric-label">Skills Detected</span>
          <div className="metric-icon-wrap" style={{ background: "#f3e8ff", color: "#9333ea" }}>
            <Cpu size={16} />
          </div>
        </div>
        <div className="metric-val">{totalResumeSkills}</div>
        <div className="metric-sub">Found in resume text</div>
      </div>

      {/* 3. Matching Skills */}
      <div className="metric-card accent-green">
        <div className="metric-header">
          <span className="metric-label">Matching Skills</span>
          <div className="metric-icon-wrap" style={{ background: "#dcfce7", color: "#16a34a" }}>
            <CheckCircle2 size={16} />
          </div>
        </div>
        <div className="metric-val">{matchingSkillsCount}</div>
        <div className="metric-sub">Overlap with JD requirements</div>
      </div>

      {/* 4. Skill Overlap */}
      <div className="metric-card accent-amber">
        <div className="metric-header">
          <span className="metric-label">Skill Overlap</span>
          <div className="metric-icon-wrap" style={{ background: "#fef3c7", color: "#d97706" }}>
            <Percent size={16} />
          </div>
        </div>
        <div className="metric-val">{overlapPct}%</div>
        <div className="metric-sub">Of JD required skills found</div>
      </div>
    </div>
  );
}
