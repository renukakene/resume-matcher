import React from "react";
import { User, Mail, Phone, GraduationCap, Briefcase, FolderGit2, Award, Cpu } from "lucide-react";

export default function ResumeInfoCard({ resumeInfo }) {
  if (!resumeInfo) return null;

  const {
    name,
    email,
    phone,
    education,
    experience,
    projects,
    certifications,
    skill_names = []
  } = resumeInfo;

  return (
    <div className="dashboard-card">
      <h3 className="dashboard-card-title">
        <User size={20} className="file-icon" />
        Extracted Resume Information
      </h3>

      {/* Basic Contact Info */}
      <div className="info-field-row">
        <span className="info-field-label">Candidate Name:</span>
        <span className="info-field-val" style={{ fontWeight: 600 }}>{name}</span>
      </div>

      <div className="info-field-row">
        <span className="info-field-label">Email:</span>
        <span className="info-field-val">
          {email !== "Not detected" ? (
            <span style={{ display: "inline-flex", alignItems: "center", gap: "0.35rem" }}>
              <Mail size={13} style={{ color: "#6366f1" }} />
              {email}
            </span>
          ) : (
            <span style={{ color: "#94a3b8", fontStyle: "italic" }}>Not detected</span>
          )}
        </span>
      </div>

      <div className="info-field-row">
        <span className="info-field-label">Phone:</span>
        <span className="info-field-val">
          {phone !== "Not detected" ? (
            <span style={{ display: "inline-flex", alignItems: "center", gap: "0.35rem" }}>
              <Phone size={13} style={{ color: "#10b981" }} />
              {phone}
            </span>
          ) : (
            <span style={{ color: "#94a3b8", fontStyle: "italic" }}>Not detected</span>
          )}
        </span>
      </div>

      {/* Education */}
      <div className="info-section-block">
        <div className="info-section-heading" style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
          <GraduationCap size={15} />
          Education
        </div>
        <div className="info-section-content">{education}</div>
      </div>

      {/* Experience */}
      <div className="info-section-block">
        <div className="info-section-heading" style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
          <Briefcase size={15} />
          Experience
        </div>
        <div className="info-section-content">{experience}</div>
      </div>

      {/* Projects */}
      <div className="info-section-block">
        <div className="info-section-heading" style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
          <FolderGit2 size={15} />
          Projects
        </div>
        <div className="info-section-content">{projects}</div>
      </div>

      {/* Certifications */}
      <div className="info-section-block">
        <div className="info-section-heading" style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
          <Award size={15} />
          Certifications
        </div>
        <div className="info-section-content">{certifications}</div>
      </div>

      {/* All Skills Detected in Resume */}
      <div className="info-section-block">
        <div className="info-section-heading" style={{ display: "flex", alignItems: "center", gap: "0.4rem" }}>
          <Cpu size={15} />
          All Skills Detected in Resume ({skill_names.length})
        </div>
        <div className="chips-container" style={{ marginTop: "0.5rem" }}>
          {skill_names.length > 0 ? (
            skill_names.map((skill) => (
              <span key={skill} className="skill-chip chip-default">
                {skill}
              </span>
            ))
          ) : (
            <span className="empty-chip-msg">No skills from dictionary detected</span>
          )}
        </div>
      </div>
    </div>
  );
}
