export default function HowItWorks({ onClose }) {
  return (
    <div className="how-it-works">
      <div className="hiw-header">
        <h2>How GougeStop Saves You Money</h2>
        <button className="hiw-close" onClick={onClose} aria-label="Close">&times;</button>
      </div>

      <p className="hiw-intro">
        Most labs charge 3 to 5 times what Medicare says your tests are worth.
        GougeStop shows you the real numbers so you can do something about it.
      </p>

      <div className="hiw-steps">
        <div className="hiw-step">
          <span className="hiw-num">1</span>
          <div>
            <strong>Snap a Photo</strong>
            <p>Take a picture of your lab bill, doctor's lab order, or ABN with your phone. GougeStop reads it right away.</p>
          </div>
        </div>

        <div className="hiw-step">
          <span className="hiw-num">2</span>
          <div>
            <strong>See What's Fair</strong>
            <p>GougeStop shows you what Medicare says each test should cost. If you uploaded a bill, you'll see the overcharge on every test in plain dollars.</p>
          </div>
        </div>

        <div className="hiw-step">
          <span className="hiw-num">3</span>
          <div>
            <strong>Compare Nearby Labs</strong>
            <p>See what up to 8 labs near you have actually charged other patients for the same tests.</p>
          </div>
        </div>

        <div className="hiw-step">
          <span className="hiw-num">4</span>
          <div>
            <strong>Get a Better Price</strong>
            <p>Haven't had your test yet? Use the Medicare rates to push back on what the lab wants to charge — before you agree to anything.</p>
          </div>
        </div>

        <div className="hiw-step">
          <span className="hiw-num">5</span>
          <div>
            <strong>Fight Unfair Charges</strong>
            <p>Already got a bill that's too high? Use GougeStop's numbers when you talk to the lab about lowering it. If they won't budge, use the data to write to the lab and Medicare about the markup.</p>
          </div>
        </div>
      </div>

      <div className="hiw-privacy">
        <strong>Your Privacy</strong>
        <p>We never save your photo, name, or personal info. The only thing we keep is pricing data — which tests, which lab, what they charged, and the general area — so we can help everyone find fairer prices.</p>
      </div>

      <button className="btn btn-primary" onClick={onClose}>
        Got It — Let's Go
      </button>
    </div>
  );
}
