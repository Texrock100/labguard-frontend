import { useState } from "react";

export default function AccessGate({ validCodes, onAccessGranted }) {
  const [code, setCode] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validCodes.includes(code.trim().toUpperCase())) {
      onAccessGranted();
    } else {
      setError("Invalid access code. Please try again.");
    }
  };

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">
            <span className="title-blood">Gouge</span>
            <span className="title-war">Stop</span>
          </h1>
          <p className="app-tagline">Know what Medicare pays. Stop overpaying.</p>
        </div>
      </header>

      <main className="app-main">
        <div className="access-gate">
          <div className="gate-card">
            <div className="gate-icon">&#x1F512;</div>
            <h2>Beta Access</h2>
            <p>LabGuard is currently in private beta. Enter your invite code to continue.</p>
            <form onSubmit={handleSubmit}>
              <input
                type="text"
                className="gate-input"
                placeholder="Enter access code"
                value={code}
                onChange={(e) => {
                  setCode(e.target.value);
                  setError("");
                }}
                autoFocus
                autoComplete="off"
              />
              {error && <div className="gate-error">{error}</div>}
              <button type="submit" className="btn btn-primary">
                Enter
              </button>
            </form>
          </div>
          <p className="gate-contact">
            Want access? Contact us at{" "}
            <a href="mailto:david@avantcapitalpartners.com">david@avantcapitalpartners.com</a>
          </p>
        </div>
      </main>

      <footer className="app-footer">
        <p>LabGuard is for informational purposes only. Not medical or financial advice.</p>
      </footer>
    </div>
  );
}
