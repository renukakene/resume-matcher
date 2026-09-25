import React from "react";
import { Cpu } from "lucide-react";

export default function Header() {
  return (
    <header className="app-header">
      <div className="header-inner">
        <div className="brand-wrapper">
          <div className="brand-icon">
            <Cpu size={18} />
          </div>
          <div className="brand-text">
            <h1>ResumeIQ</h1>
            <p className="brand-subtitle">Resume & Job Description Analyzer</p>
          </div>
        </div>
      </div>
    </header>
  );
}
