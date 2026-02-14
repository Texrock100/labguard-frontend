import { useState } from "react";
import CaptureScreen from "./components/CaptureScreen";
import ResultsScreen from "./components/ResultsScreen";
import LoadingScreen from "./components/LoadingScreen";
import ErrorScreen from "./components/ErrorScreen";
import AccessGate from "./components/AccessGate";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "https://web-production-c5039.up.railway.app";

// Valid invite codes - add more as needed
const VALID_CODES = ["GOUGESTOP2026", "BETAUSER", "BADGER"];

function App() {
  const [screen, setScreen] = useState("capture");
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [state, setState] = useState("TX");
  const [hasAccess, setHasAccess] = useState(false);

  const handleAccessGranted = () => {
    setHasAccess(true);
  };

  const handleSubmit = async (imageFile) => {
    setScreen("loading");
    setError(null);

    const formData = new FormData();
    formData.append("file", imageFile);

    try {
      const resp = await fetch(`${API_URL}/analyze?state=${state}`, {
        method: "POST",
        body: formData,
      });

      if (!resp.ok) {
        const errData = await resp.json().catch(() => ({}));
        throw new Error(errData.detail || `Server error: ${resp.status}`);
      }

      const data = await resp.json();

      if (!data.success) {
        throw new Error(data.error || "Analysis failed. Please try again.");
      }

      setResults(data);
      setScreen("results");
    } catch (err) {
      setError(err.message);
      setScreen("error");
    }
  };

  const handleReset = () => {
    setResults(null);
    setError(null);
    setScreen("capture");
  };

  // Show access gate if not authenticated
  if (!hasAccess) {
    return <AccessGate validCodes={VALID_CODES} onAccessGranted={handleAccessGranted} />;
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title" onClick={handleReset}>
            <span className="title-blood">Gouge</span>
            <span className="title-war">Stop</span>
          </h1>
          <p className="app-tagline">Know what Medicare pays. Stop overpaying.</p>
        </div>
      </header>

      <main className="app-main">
        {screen === "capture" && (
          <CaptureScreen
            onSubmit={handleSubmit}
            state={state}
            onStateChange={setState}
          />
        )}
        {screen === "loading" && <LoadingScreen />}
        {screen === "results" && (
          <ResultsScreen results={results} onReset={handleReset} />
        )}
        {screen === "error" && (
          <ErrorScreen error={error} onRetry={handleReset} />
        )}
      </main>

      <footer className="app-footer">
        <p>GougeStop is for informational purposes only. Not medical or financial advice.</p>
      </footer>
    </div>
  );
}

export default App;
