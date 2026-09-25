import React from "react";
import { CheckCircle2, AlertTriangle, PlusCircle, Briefcase } from "lucide-react";

export default function SkillComparisonSection({ skillComparison, jdInfo }) {
  if (!skillComparison) return null;

  const {
    matching_skills = [],
    missing_skills = [],
    additional_skills = [],
    matching_count = 0,
    missing_count = 0,
    additional_count = 0,
    skill_overlap_percentage = 0
  } = skillComparison;

  const jdSkills = jdInfo?.skill_names || [];

  return (
    <div className="skills-comparison-wrapper" style={{ marginBottom: "2rem" }}>
      {/* 3 Columns: Matching, Missing, Additional */}
      <div className="comparison-grid">
        {/* Column 1: Matching Skills */}
        <div className="breakdown-card matching">
          <div className="breakdown-header">
            <div className="breakdown-title-group">
              <CheckCircle2 size={18} style={{ color: "var(--success)" }} />
              <h4 className="breakdown-title">Matching Skills</h4>
            </div>
            <span className="count-pill pill-green">{matching_count}</span>
          </div>
          <div className="chips-container">
            {matching_skills.length > 0 ? (
              matching_skills.map((skill) => (
                <span key={skill} className="skill-chip chip-match">
                  <CheckCircle2 size={12} />
                  {skill}
                </span>
              ))
            ) : (
              <span className="empty-chip-msg">No matching skills detected between resume & JD</span>
            )}
          </div>
        </div>

        {/* Column 2: Missing Skills (In JD, not in Resume) */}
        <div className="breakdown-card missing">
          <div className="breakdown-header">
            <div className="breakdown-title-group">
              <AlertTriangle size={18} style={{ color: "var(--warning)" }} />
              <h4 className="breakdown-title">Missing From Resume</h4>
            </div>
            <span className="count-pill pill-amber">{missing_count}</span>
          </div>
          <div className="chips-container">
            {missing_skills.length > 0 ? (
              missing_skills.map((skill) => (
                <span key={skill} className="skill-chip chip-missing">
                  <AlertTriangle size={12} />
                  {skill}
                </span>
              ))
            ) : (
              <span className="empty-chip-msg">All detected JD skills were found in resume!</span>
            )}
          </div>
        </div>

        {/* Column 3: Additional Resume Skills (In Resume, not in JD) */}
        <div className="breakdown-card additional">
          <div className="breakdown-header">
            <div className="breakdown-title-group">
              <PlusCircle size={18} style={{ color: "var(--info)" }} />
              <h4 className="breakdown-title">Additional Resume Skills</h4>
            </div>
            <span className="count-pill pill-blue">{additional_count}</span>
          </div>
          <div className="chips-container">
            {additional_skills.length > 0 ? (
              additional_skills.map((skill) => (
                <span key={skill} className="skill-chip chip-additional">
                  <PlusCircle size={12} />
                  {skill}
                </span>
              ))
            ) : (
              <span className="empty-chip-msg">No extra skills detected</span>
            )}
          </div>
        </div>
      </div>

      {/* JD Skills Overview Strip */}
      <div className="dashboard-card" style={{ marginTop: "1rem" }}>
        <div className="breakdown-header" style={{ marginBottom: "0.75rem" }}>
          <div className="breakdown-title-group">
            <Briefcase size={18} style={{ color: "var(--primary)" }} />
            <h4 className="breakdown-title">All Skills Required in Job Description ({jdSkills.length})</h4>
          </div>
          <span style={{ fontSize: "0.8rem", color: "var(--text-muted)" }}>
            Skill Overlap: <strong>{skill_overlap_percentage}%</strong>
          </span>
        </div>
        <div className="chips-container">
          {jdSkills.length > 0 ? (
            jdSkills.map((skill) => {
              const isMatch = matching_skills.includes(skill);
              return (
                <span
                  key={skill}
                  className={`skill-chip ${isMatch ? "chip-match" : "chip-missing"}`}
                  title={isMatch ? "Matched in resume" : "Missing in resume"}
                >
                  {isMatch ? <CheckCircle2 size={12} /> : <AlertTriangle size={12} />}
                  {skill}
                </span>
              );
            })
          ) : (
            <span className="empty-chip-msg">No skills from the dictionary detected in this job description.</span>
          )}
        </div>
      </div>
    </div>
  );
}
