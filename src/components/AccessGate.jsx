import { useState, useEffect } from "react";

const API_URL = import.meta.env.VITE_API_URL || "https://web-production-c5039.up.railway.app";

// Keep invite codes as a fallback
const VALID_CODES = ["GOUGESTOP2026", "BETAUSER", "BADGER"];

export default function AccessGate({ onAccessGranted }) {
  const [mode, setMode] = useState("email"); // "email" | "code-sent" | "invite"
  const [email, setEmail] = useState("");
  const [verifyCode, setVerifyCode] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [checking, setChecking] = useState(true);

  // On mount, check for existing session token
  useEffect(() => {
    const token = localStorage.getItem("gs_token");
    if (token) {
      fetch(`${API_URL}/auth/check-token`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ token }),
      })
        .then((r) => r.json())
        .then((data) => {
          if (data.valid) {
            onAccessGranted();
          } else {
            localStorage.removeItem("gs_token");
            setChecking(false);
          }
        })
        .catch(() => {
          setChecking(false);
        });
    } else {
      setChecking(false);
    }
  }, []);

  const handleSendCode = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const resp = await fetch(`${API_URL}/auth/send-code`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim() }),
      });

      if (!resp.ok) {
        const data = await resp.json().catch(() => ({}));
        throw new Error(data.detail || "Failed to send code.");
      }

      setMode("code-sent");
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyCode = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      const resp = await fetch(`${API_URL}/auth/verify-code`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email: email.trim(), code: verifyCode.trim() }),
      });

      const data = await resp.json().catch(() => ({}));

      if (!resp.ok) {
        throw new Error(data.detail || "Verification failed.");
      }

      if (data.token) {
        localStorage.setItem("gs_token", data.token);
      }

      onAccessGranted();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleInviteCode = (e) => {
    e.preventDefault();
    if (VALID_CODES.includes(verifyCode.trim().toUpperCase())) {
      onAccessGranted();
    } else {
      setError("Invalid access code. Please try again.");
    }
  };

  // Show nothing while checking token
  if (checking) {
    return (
      <div className="app">
        <header className="app-header">
          <div className="header-content">
            <h1 className="app-title">
              <span className="title-blood">Gouge</span>
              <span className="title-war">Stop</span>
            </h1>
          </div>
        </header>
        <main className="app-main">
          <div className="loading-screen">
            <div className="spinner"></div>
          </div>
        </main>
      </div>
    );
  }

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
            <div className="gate-icon">&#x1F6E1;&#xFE0F;</div>

            {mode === "email" && (
              <>
                <h2>Get Started</h2>
                <p>Enter your email to access GougeStop. We'll send you a quick verification code.</p>
                <form onSubmit={handleSendCode}>
                  <input
                    type="email"
                    className="gate-input"
                    placeholder="your@email.com"
                    value={email}
                    onChange={(e) => {
                      setEmail(e.target.value);
                      setError("");
                    }}
                    autoFocus
                    autoComplete="email"
                    style={{ textTransform: "none", letterSpacing: "normal" }}
                  />
                  {error && <div className="gate-error">{error}</div>}
                  <button type="submit" className="btn btn-primary" disabled={loading || !email.trim()}>
                    {loading ? "Sending..." : "Send Code"}
                  </button>
                </form>
                <button
                  className="gate-toggle"
                  onClick={() => { setMode("invite"); setError(""); }}
                >
                  Have an invite code?
                </button>
              </>
            )}

            {mode === "code-sent" && (
              <>
                <h2>Check Your Email</h2>
                <p>We sent a 6-digit code to <strong>{email}</strong>. Enter it below.</p>
                <form onSubmit={handleVerifyCode}>
                  <input
                    type="text"
                    className="gate-input"
                    placeholder="000000"
                    value={verifyCode}
                    onChange={(e) => {
                      const val = e.target.value.replace(/\D/g, "").slice(0, 6);
                      setVerifyCode(val);
                      setError("");
                    }}
                    autoFocus
                    inputMode="numeric"
                    autoComplete="one-time-code"
                  />
                  {error && <div className="gate-error">{error}</div>}
                  <button type="submit" className="btn btn-primary" disabled={loading || verifyCode.length < 6}>
                    {loading ? "Verifying..." : "Verify"}
                  </button>
                </form>
                <button
                  className="gate-toggle"
                  onClick={() => { setMode("email"); setError(""); setVerifyCode(""); }}
                >
                  Use a different email
                </button>
              </>
            )}

            {mode === "invite" && (
              <>
                <h2>Beta Access</h2>
                <p>Enter your invite code to continue.</p>
                <form onSubmit={handleInviteCode}>
                  <input
                    type="text"
                    className="gate-input"
                    placeholder="Enter access code"
                    value={verifyCode}
                    onChange={(e) => {
                      setVerifyCode(e.target.value);
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
                <button
                  className="gate-toggle"
                  onClick={() => { setMode("email"); setError(""); setVerifyCode(""); }}
                >
                  Use email instead
                </button>
              </>
            )}
          </div>

          <p className="gate-contact">
            Questions? Contact us at{" "}
            <a href="mailto:info@gougestop.com">info@gougestop.com</a>
          </p>
        </div>
      </main>

      <footer className="app-footer">
        <p>GougeStop is for informational purposes only. Not medical or financial advice.</p>
      </footer>
    </div>
  );
}
