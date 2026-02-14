export default function ErrorScreen({ error, onRetry }) {
  return (
    <div className="error-screen">
      <div className="error-icon">&#9888;&#65039;</div>
      <h2>Something Went Wrong</h2>
      <p>{error}</p>
      <button className="btn btn-primary" onClick={onRetry}>
        Try Again
      </button>
    </div>
  );
}
