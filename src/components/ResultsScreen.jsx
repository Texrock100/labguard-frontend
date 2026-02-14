import { useState } from "react";

function fmt(num) {
  if (num == null) return "N/A";
  return "$" + num.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
}

function pct(num) {
  if (num == null) return "";
  const sign = num > 0 ? "+" : "";
  return sign + num.toFixed(1) + "%";
}

export default function ResultsScreen({ results, onReset }) {
  const [expandedLab, setExpandedLab] = useState(null);
  const r = results;

  const docLabel = {
    bill: "Bill",
    order: "Order",
    abn: "ABN",
  }[r.document_type] || "Document";

  const hasBillData = r.document_type === "bill" || r.document_type === "abn";

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

      {/* Scan again */}
      <div className="scan-again">
        <button className="btn btn-secondary" onClick={onReset}>
          Scan Another Document
        </button>
      </div>
    </div>
  );
}
