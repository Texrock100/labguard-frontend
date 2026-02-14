import { useState, useEffect } from "react";

const STEPS = [
  "Reading your document...",
  "Identifying test codes...",
  "Looking up Medicare rates...",
  "Finding nearby lab prices...",
];

export default function LoadingScreen() {
  const [activeStep, setActiveStep] = useState(0);

  useEffect(() => {
    const timer = setInterval(() => {
      setActiveStep((prev) => (prev < STEPS.length - 1 ? prev + 1 : prev));
    }, 2500);
    return () => clearInterval(timer);
  }, []);

  return (
    <div className="loading-screen">
      <div className="spinner" />
      <h2>Analyzing Your Document</h2>
      <p>This usually takes 5-10 seconds</p>
      <div className="loading-steps">
        {STEPS.map((step, i) => (
          <div
            key={i}
            className={`loading-step ${
              i < activeStep ? "done" : i === activeStep ? "active" : ""
            }`}
          >
            <span>{i < activeStep ? "\u2713" : i === activeStep ? "\u25CB" : "\u00B7"}</span>
            <span>{step}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
