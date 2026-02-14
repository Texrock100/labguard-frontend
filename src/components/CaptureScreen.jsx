import { useState, useRef } from "react";

const US_STATES = [
  "AL","AK","AZ","AR","CA","CO","CT","DE","FL","GA","HI","ID","IL","IN","IA",
  "KS","KY","LA","ME","MD","MA","MI","MN","MS","MO","MT","NE","NV","NH","NJ",
  "NM","NY","NC","ND","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VT",
  "VA","WA","WV","WI","WY","DC","PR",
];

export default function CaptureScreen({ onSubmit, state, onStateChange }) {
  const [file, setFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [dragOver, setDragOver] = useState(false);
  const inputRef = useRef();

  const handleFile = (f) => {
    if (!f) return;
    setFile(f);
    const reader = new FileReader();
    reader.onload = (e) => setPreview(e.target.result);
    reader.readAsDataURL(f);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const f = e.dataTransfer.files[0];
    if (f) handleFile(f);
  };

  const handleClear = () => {
    setFile(null);
    setPreview(null);
    if (inputRef.current) inputRef.current.value = "";
  };

  return (
    <div className="capture-screen">
      {/* Instructions */}
      <div className="capture-instructions">
        <h2>Scan Your Lab Document</h2>
        <ol className="step-list">
          <li>
            <span className="step-number">1</span>
            <span>Take a photo or upload your lab document</span>
          </li>
          <li>
            <span className="step-number">2</span>
            <span>Select your state for nearby lab pricing</span>
          </li>
          <li>
            <span className="step-number">3</span>
            <span>Tap <strong>Analyze</strong> to see your results</span>
          </li>
        </ol>
        <div className="doc-types">
          <span className="doc-type-tag">Blood Test Order</span>
          <span className="doc-type-tag">Lab Bill</span>
          <span className="doc-type-tag">ABN</span>
        </div>
      </div>

      {/* State selector */}
      <div className="state-selector">
        <label htmlFor="state-select">Your State:</label>
        <select
          id="state-select"
          value={state}
          onChange={(e) => onStateChange(e.target.value)}
        >
          {US_STATES.map((s) => (
            <option key={s} value={s}>{s}</option>
          ))}
        </select>
      </div>

      {/* Upload / Camera zone */}
      {!preview ? (
        <div
          className={`upload-zone ${dragOver ? "drag-over" : ""}`}
          onClick={() => inputRef.current?.click()}
          onDrop={handleDrop}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
        >
          <div className="upload-icon">📷</div>
          <h3>Take Photo or Upload</h3>
          <p>Tap to open camera or choose a file</p>
          <input
            ref={inputRef}
            className="upload-input"
            type="file"
            accept="image/*,application/pdf"
            capture="environment"
            onChange={(e) => handleFile(e.target.files[0])}
          />
        </div>
      ) : (
        <div className="preview-section">
          <img src={preview} alt="Document preview" className="preview-image" />
          <div className="preview-actions">
            <button className="btn btn-secondary btn-small" onClick={handleClear}>
              Change Photo
            </button>
            <button
              className="btn btn-primary btn-small"
              onClick={() => onSubmit(file)}
            >
              Analyze Document
            </button>
          </div>
        </div>
      )}

      {/* Big analyze button when file selected */}
      {preview && (
        <button className="btn btn-primary" onClick={() => onSubmit(file)}>
          Analyze My Lab Document
        </button>
      )}
    </div>
  );
}
