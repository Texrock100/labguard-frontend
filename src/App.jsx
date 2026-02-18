import { useState, useEffect } from "react";
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
  const [isPaid, setIsPaid] = useState(false);
  const [checkoutLoading, setCheckoutLoading] = useState(false);

  // Check for payment success in URL
  useEffect(() => {
    const params = new URLSearchParams(window.location.search);
    if (params.get("payment") === "success") {
      setIsPaid(true);
      setScansRemaining(-1);
      // Clean URL
      window.history.replaceState({}, "", window.location.pathname);
    }
  }, []);

  const handleAccessGranted = () => {
    setHasAccess(true);
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
            setIsPaid(data.is_paid);
          }
        })
        .catch(() => {});
    }
  };

  const handleUpgrade = async () => {
    setCheckoutLoading(true);
    const token = localStorage.getItem("gs_token");
    if (!token) {
      setCheckoutLoading(false);
      return;
    }

    try {
      const resp = await fetch(`${API_URL}/stripe/create-checkout`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token }),
      });

      const data = await resp.json();

      if (data.checkout_url) {
        window.location.href = data.checkout_url;
      } else {
        setCheckoutLoading(false);
      }
    } catch {
      setCheckoutLoading(false);
    }
  };

  const handleSubmit = async (imageFile) => {
    setScreen("loading");
    setError(null);

    const formData = new FormData();
    formData.append("file", imageFile);

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
          setScreen("paywall");
          return;
        }
        throw new Error(errData.detail || `Server error: ${resp.status}`);
      }

      const data = await resp.json();

      if (!data.success) {
        throw new Error(data.error || "Analysis failed. Please try again.");
      }

      if (scansRemaining !== null && scansRemaining > 0) {
        setScansRemaining(scansRemaining - 1);
      }

      setResults(data);
      setScreen("results");

      // GA4: Track successful scan
      if (window.gtag) {
        window.gtag('event', 'scan_completed', {
          document_type: data.document_type || 'unknown',
          tests_found: data.items ? data.items.length : 0,
          has_markup: data.total_markup != null,
        });
      }
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
        {screen === "paywall" && (
          <div className="paywall-screen">
            <div className="paywall-card">
              <div className="paywall-icon">&#x1F513;</div>
              <h2>Unlock Unlimited Scans</h2>
              <p>You've used your 3 free scans. Upgrade to keep using GougeStop and save on every lab bill.</p>
              <div className="paywall-price">
                <span className="paywall-amount">$4.99</span>
                <span className="paywall-period">one-time</span>
              </div>
              <ul className="paywall-features">
                <li>Unlimited bill and order scans</li>
                <li>Compare prices at nearby labs</li>
                <li>See Medicare rates for every test</li>
                <li>Negotiate with real numbers</li>
              </ul>
              <button
                className="btn btn-primary paywall-btn"
                onClick={handleUpgrade}
                disabled={checkoutLoading}
              >
                {checkoutLoading ? "Loading..." : "Upgrade Now — $4.99"}
              </button>
              <button className="gate-toggle" onClick={handleReset}>
                Back
              </button>
            </div>
          </div>
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
