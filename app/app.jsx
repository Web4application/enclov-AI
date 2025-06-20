import React, { useState } from "react";

export default function App() {
  const [code, setCode] = useState("");
  const [review, setReview] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setReview("");

    try {
      const res = await fetch("/analyze-code", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ code }),
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Unknown error");
      }

      const data = await res.json();
      setReview(data.review_comment);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>enclov-AI Code Reviewer</h1>
      <form onSubmit={handleSubmit} style={styles.form}>
        <textarea
          placeholder="Paste your code snippet here..."
          value={code}
          onChange={(e) => setCode(e.target.value)}
          rows={10}
          style={styles.textarea}
          required
        />
        <button type="submit" style={styles.button} disabled={loading}>
          {loading ? "Reviewing..." : "Review Code"}
        </button>
      </form>
      {error && <p style={styles.error}>Error: {error}</p>}
      {review && (
        <div style={styles.reviewBox}>
          <h2>AI Review</h2>
          <pre style={styles.pre}>{review}</pre>
        </div>
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: 700,
    margin: "2rem auto",
    fontFamily: "'Segoe UI', Tahoma, Geneva, Verdana, sans-serif",
    color: "#121212",
  },
  title: {
    textAlign: "center",
    color: "#4caf50",
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
  },
  textarea: {
    fontFamily: "monospace",
    fontSize: "1rem",
    padding: "1rem",
    borderRadius: 6,
    border: "1px solid #ccc",
    resize: "vertical",
  },
  button: {
    backgroundColor: "#4caf50",
    color: "#fff",
    border: "none",
    padding: "1rem",
    borderRadius: 6,
    fontWeight: "bold",
    cursor: "pointer",
  },
  error: {
    color: "red",
    marginTop: "1rem",
  },
  reviewBox: {
    marginTop: "2rem",
    backgroundColor: "#f0f0f0",
    borderRadius: 6,
    padding: "1rem",
    whiteSpace: "pre-wrap",
  },
  pre: {
    fontFamily: "monospace",
    fontSize: "1rem",
  },
};
