import { useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "https://web-production-c5039.up.railway.app";

function fmt(num) {
  if (num == null) return "N/A";
  return "$" + num.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function pct(num) {
  if (num == null) return "";
  const sign = num > 0 ? "+" : "";
  return sign + Math.round(num) + "%";
}

function buildResultsHTML(r) {
  const docLabel = { bill: "Bill", order: "Order", abn: "ABN" }[r.document_type] || "Document";
  const hasBillData = r.document_type === "bill" || r.document_type === "abn";

  let html = `<h2 style="color:#1B3A5C;font-size:20px;margin-bottom:12px;">Your GougeStop Results</h2>`;

  if (r.provider_name || r.date_of_service) {
    html += `<p style="color:#6c757d;font-size:14px;margin-bottom:16px;">`;
    if (r.provider_name) html += r.provider_name;
    if (r.provider_name && r.date_of_service) html += ` &middot; `;
    if (r.date_of_service) html += r.date_of_service;
    html += ` (${docLabel})</p>`;
  }

  // Totals
  html += `<div style="display:flex;gap:12px;flex-wrap:wrap;margin-bottom:20px;">`;
  html += `<div style="flex:1;min-width:120px;background:#d4edda;border-radius:8px;padding:12px;text-align:center;">`;
  html += `<div style="font-size:11px;font-weight:600;color:#495057;text-transform:uppercase;">Medicare Allows</div>`;
  html += `<div style="font-size:22px;font-weight:700;color:#28a745;">${fmt(r.total_medicare_allowed)}</div></div>`;

  if (hasBillData && r.total_provider_charges) {
    html += `<div style="flex:1;min-width:120px;background:#f8d7da;border-radius:8px;padding:12px;text-align:center;">`;
    html += `<div style="font-size:11px;font-weight:600;color:#495057;text-transform:uppercase;">Provider Charged</div>`;
    html += `<div style="font-size:22px;font-weight:700;color:#dc3545;">${fmt(r.total_provider_charges)}</div></div>`;
  }
  html += `</div>`;

  if (hasBillData && r.total_markup != null) {
    html += `<div style="background:#ffecd2;border-radius:8px;padding:12px;text-align:center;margin-bottom:20px;">`;
    html += `<div style="font-size:11px;font-weight:600;color:#495057;text-transform:uppercase;">You Were Overcharged</div>`;
    html += `<div style="font-size:22px;font-weight:700;color:#e67e22;">${fmt(r.total_markup)}</div>`;
    if (r.average_markup_percent != null) {
      html += `<div style="font-size:12px;color:#6c757d;">Average markup: ${pct(r.average_markup_percent)}</div>`;
    }
    html += `</div>`;
  }

  // Line items
  html += `<h3 style="color:#1B3A5C;font-size:16px;margin-bottom:12px;">Test-by-Test Breakdown</h3>`;
  html += `<table style="width:100%;border-collapse:collapse;font-size:14px;">`;
  html += `<tr style="border-bottom:2px solid #dee2e6;"><th style="text-align:left;padding:8px 4px;">Test</th>`;
  html += `<th style="text-align:right;padding:8px 4px;">Medicare</th>`;
  if (hasBillData) html += `<th style="text-align:right;padding:8px 4px;">Charged</th>`;
  html += `</tr>`;

  for (const item of r.items) {
    html += `<tr style="border-bottom:1px solid #e9ecef;">`;
    html += `<td style="padding:8px 4px;"><strong>${item.cpt_code}</strong> ${item.test_description || ""}</td>`;
    html += `<td style="text-align:right;padding:8px 4px;color:#28a745;font-weight:600;">${fmt(item.medicare_allowed)}</td>`;
    if (hasBillData) {
      html += `<td style="text-align:right;padding:8px 4px;color:#dc3545;font-weight:600;">${item.provider_charge != null ? fmt(item.provider_charge) : "—"}</td>`;
    }
    html += `</tr>`;
  }
  html += `</table>`;

  return html;
}

export default function ResultsScreen({ results, onReset }) {
  const [expandedLab, setExpandedLab] = useState(null);
  const [showShare, setShowShare] = useState(false);
  const [shareEmail, setShareEmail] = useState("");
  const [shareSending, setShareSending] = useState(false);
  const [shareMsg, setShareMsg] = useState("");
  const r = results;

  const docLabel = {
    bill: "Bill",
    order: "Order",
    abn: "ABN",
  }[r.document_type] || "Document";

  const hasBillData = r.document_type === "bill" || r.document_type === "abn";

  const handleShare = async () => {
    if (!shareEmail.trim() || !shareEmail.includes("@")) {
      setShareMsg("Please enter a valid email address.");
      return;
    }

    setShareSending(true);
    setShareMsg("");

    const token = localStorage.getItem("gs_token") || "";

    try {
      const resp = await fetch(`${API_URL}/share-results`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          token,
          recipient_email: shareEmail.trim(),
          results_html: buildResultsHTML(r),
        }),
      });

      const data = await resp.json();

      if (resp.ok && data.success) {
        setShareMsg("Sent! Check your inbox.");
        setTimeout(() => {
          setShowShare(false);
          setShareMsg("");
          setShareEmail("");
        }, 2000);
      } else {
        setShareMsg(data.detail || "Failed to send. Please try again.");
      }
    } catch {
      setShareMsg("Failed to send. Please try again.");
    } finally {
      setShareSending(false);
    }
  };

  return (
    <div className="results-screen">
      {/* Summary Card */}
      <div className="summary-card">
        <div className="summary-header">
          <h2>Your Results</h2>
          <span className={`doc-badge ${r.document_type}`}>{docLabel}</span>
        </div>

        {(r.provider_name || r.date_of_service) && (
          <div className="summary-meta">
            {r.provider_name && <span>{r.provider_name}</span>}
            {r.provider_name && r.date_of_service && <span> &middot; </span>}
            {r.date_of_service && <span>{r.date_of_service}</span>}
          </div>
        )}

        <div className="summary-totals">
          <div className="total-box medicare">
            <div className="total-label">Medicare Allows</div>
            <div className="total-value">{fmt(r.total_medicare_allowed)}</div>
          </div>

          {hasBillData && r.total_provider_charges && (
            <div className="total-box provider">
              <div className="total-label">Provider Charged</div>
              <div className="total-value">{fmt(r.total_provider_charges)}</div>
            </div>
          )}

          {hasBillData && r.total_markup != null && (
            <div className="total-box markup">
              <div className="total-label">You Were Overcharged</div>
              <div className="total-value">{fmt(r.total_markup)}</div>
              {r.average_markup_percent != null && (
                <div className="total-sub">
                  Average markup: {pct(r.average_markup_percent)}
                </div>
              )}
            </div>
          )}

          {!hasBillData && (
            <div className="total-box provider" style={{ background: "#d1ecf1" }}>
              <div className="total-label">Tests Found</div>
              <div className="total-value" style={{ color: "#0c5460" }}>
                {r.items.length}
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Line Items */}
      <div className="items-card">
        <h3>Test-by-Test Breakdown</h3>
        {r.items.map((item, i) => (
          <div className="item-row" key={i}>
            <div className="item-header">
              <span className="item-cpt">{item.cpt_code}</span>
              {item.markup_percent != null && (
                <span className={`item-markup ${item.markup_percent > 0 ? "positive" : "negative"}`}>
                  {pct(item.markup_percent)} markup
                </span>
              )}
            </div>
            <div className="item-desc">
              {item.test_description}
              {item.medicare_description && item.medicare_description !== item.test_description && (
                <> &mdash; {item.medicare_description}</>
              )}
            </div>
            <div className="item-prices">
              <div>
                <div className="item-price-label">Medicare Allows</div>
                <div className="item-price-val medicare">{fmt(item.medicare_allowed)}</div>
              </div>
              {hasBillData && item.provider_charge != null && (
                <div>
                  <div className="item-price-label">Provider Charged</div>
                  <div className="item-price-val provider">{fmt(item.provider_charge)}</div>
                </div>
              )}
              {item.markup_dollars != null && (
                <div>
                  <div className="item-price-label">Overcharge</div>
                  <div className="item-price-val provider">{fmt(item.markup_dollars)}</div>
                </div>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Nearby Labs */}
      {r.nearby_labs && r.nearby_labs.length > 0 && (
        <div className="labs-card">
          <h3>Nearby Labs &mdash; Estimated Total</h3>
          <p className="labs-subtitle">
            Tap a lab to see per-test pricing. Based on 2023 Medicare claims data.
          </p>
          {r.nearby_labs.map((lab, i) => (
            <div
              className={`lab-row ${expandedLab === i ? "expanded" : ""}`}
              key={i}
              onClick={() => setExpandedLab(expandedLab === i ? null : i)}
            >
              <div className="lab-main">
                <div>
                  <div className="lab-name">
                    <span className={`lab-rank ${i === 0 ? "best" : ""}`}>{i + 1}</span>
                    {lab.provider_name}
                  </div>
                  <div className="lab-city">{lab.provider_city}</div>
                </div>
                <div className="lab-total">
                  <div className="lab-price">{fmt(lab.estimated_total)}</div>
                  <div className="lab-codes">
                    {lab.codes_priced}/{lab.codes_requested} tests priced
                  </div>
                </div>
              </div>

              {/* Expanded detail */}
              {expandedLab === i && lab.charges_by_code && (
                <div className="lab-detail">
                  {Object.entries(lab.charges_by_code).map(([code, info]) => (
                    <div className="lab-detail-row" key={code}>
                      <span className="lab-detail-code">
                        {code} {info.description ? `- ${info.description}` : ""}
                      </span>
                      <span className="lab-detail-charge">{fmt(info.charge)}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Disclaimer */}
      <p className="disclaimer">{r.data_disclaimer}</p>

      {/* Action Buttons */}
      <div className="results-actions">
        <button className="btn btn-primary" onClick={() => setShowShare(true)}>
          Email These Results
        </button>
        <button className="btn btn-secondary" onClick={onReset}>
          Scan Another Document
        </button>
      </div>

      {/* Share Modal */}
      {showShare && (
        <div className="share-overlay" onClick={() => { setShowShare(false); setShareMsg(""); }}>
          <div className="share-modal" onClick={(e) => e.stopPropagation()}>
            <h3>Email Your Results</h3>
            <p>Send a copy to yourself, your doctor, or a friend.</p>
            <input
              type="email"
              className="share-input"
              placeholder="Enter email address"
              value={shareEmail}
              onChange={(e) => setShareEmail(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleShare()}
              autoFocus
            />
            {shareMsg && (
              <div className={`share-msg ${shareMsg.includes("Sent") ? "success" : "error"}`}>
                {shareMsg}
              </div>
            )}
            <button
              className="btn btn-primary"
              onClick={handleShare}
              disabled={shareSending}
            >
              {shareSending ? "Sending..." : "Send Results"}
            </button>
            <button className="gate-toggle" onClick={() => { setShowShare(false); setShareMsg(""); }}>
              Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
