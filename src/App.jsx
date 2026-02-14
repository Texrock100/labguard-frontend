import { useState } from "react";
import CaptureScreen from "./components/CaptureScreen";
import ResultsScreen from "./components/ResultsScreen";
import LoadingScreen from "./components/LoadingScreen";
import ErrorScreen from "./components/ErrorScreen";
import AccessGate from "./components/AccessGate";
import "./App.css";

const API_URL = import.meta.env.VITE_API_URL || "https://web-production-c5039.up.railway.app";

function App() {
  const [screen, setScreen] = useState("capture");
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [state, setState] = useState("TX");
  const [hasAccess, setHasAccess] = useState(false);
  const [scansRemaining, setScansRemaining] = useState(null);

  const handleAccessGranted = () => {
    setHasAccess(true);
    // Fetch initial usage
    const token = localStorage.getItem("gs_token");
    if (token) {
      fetch(`${API_URL}/auth/usage`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token }),
      })
        .then((r) => r.json())
        .then((data) => {
          if (data.scans_remaining !== undefined) {
            setScansRemaining(data.is_paid ? -1 : data.scans_remaining);
          }
        })
        .catch(() => {});
    }
  };

  const handleSubmit = async (imageFile) => {
    setScreen("loading");
    setError(null);

    const formData = new FormData();
    formData.append("file", imageFile);

    // Include token in the request for usage tracking
    const token = localStorage.getItem("gs_token") || "";
    const tokenParam = token ? `&token=${encodeURIComponent(token)}` : "";

    try {
      const resp = await fetch(`${API_URL}/analyze?state=${state}${tokenParam}`, {
        method: "POST",
        body: formData,
      });

      if (!resp.ok) {
        const errData = await resp.json().catch(() => ({}));
        if (resp.status === 403) {
          setError("limit_reached");
          setScreen("error");
          return;
        }
        throw new Error(errData.detail || `Server error: ${resp.status}`);
      }

      const data = await resp.json();

      if (!data.success) {
        throw new Error(data.error || "Analysis failed. Please try again.");
      }

      // Update remaining scans
      if (scansRemaining !== null && scansRemaining > 0) {
        setScansRemaining(scansRemaining - 1);
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
    return <AccessGate onAccessGranted={handleAccessGranted} />;
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
          <>
            {scansRemaining !== null && scansRemaining >= 0 && (
              <div className="scans-remaining">
                {scansRemaining > 0
                  ? `${scansRemaining} free scan${scansRemaining === 1 ? "" : "s"} remaining`
                  : "No free scans remaining"}
              </div>
            )}
            <CaptureScreen
              onSubmit={handleSubmit}
              state={state}
              onStateChange={setState}
            />
          </>
        )}
        {screen === "loading" && <LoadingScreen />}
        {screen === "results" && (
          <ResultsScreen results={results} onReset={handleReset} />
        )}
        {screen === "error" && (
          <ErrorScreen
            error={error === "limit_reached"
              ? "You've used all 3 free scans. Subscription coming soon — contact info@gougestop.com for more access."
              : error}
            onRetry={handleReset}
          />
        )}
      </main>

      <footer className="app-footer">
        <p>GougeStop is for informational purposes only. Not medical or financial advice.</p>
      </footer>
    </div>
  );
}

export default App;
