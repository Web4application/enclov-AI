import React, { useEffect, useState } from "react";
import "./Home.css"; // External CSS is cleaner for Vite/Next — optional

const Home = () => {
  const [progress, setProgress] = useState(0);
  const [commentsHtml, setCommentsHtml] = useState("🔄 Waiting for review...");

  useEffect(() => {
    let interval: NodeJS.Timeout;
    let current = 0;

    const simulateJobProgress = () => {
      interval = setInterval(() => {
        if (current >= 100) {
          clearInterval(interval);
          setCommentsHtml(`
            <strong>AI Review Comments:</strong><br/><br/>
            ✅ Refactored inefficient loop at <code>utils/helpers.py:45</code>.<br/>
            🛡️ Suggested stronger typing in <code>main.py</code>.<br/>
            🧹 Cleaned unused imports in <code>api/views.py</code>.<br/>
            🔒 Security tip: avoid exposing tokens in logs.<br/>
          `);
        } else {
          current += Math.random() * 10;
          setProgress(Math.min(current, 100));
          setCommentsHtml(`<strong>AI Review Comments:</strong><br/><br/><em>Analyzing diffs... (${Math.floor(current)}%)</em>`);
        }
      }, 600);
    };

    simulateJobProgress();
  }, []);

  return (
    <div className="container">
      <header className="header">
        <div className="logo">QUBUHUB</div>
        <nav className="menu">
          <a href="https://web4application.github.io/kubu-hai" target="_blank" rel="noreferrer">kubu-hai</a>
          <a href="https://github.com/Web4application/enclov-AI" target="_blank" rel="noreferrer">GitHub</a>
          <a href="#">Products</a>
          <a href="#">Careers</a>
        </nav>
      </header>

      <main>
        <h1>enclov-AI</h1>
        <p className="lead">
          Supercharge your GitHub PR workflow with real-time AI-powered review automation.<br />
          Powered by OpenAI, FastAPI, Redis, Celery, and the unstoppable drive of QUBUHUB.
        </p>

        <a className="button" href="https://github.com/Web4application/enclov-AI" target="_blank" rel="noreferrer">
          View on GitHub
        </a>

        <div className="progress-container">
          <div className="progress-bar" style={{ width: `${progress}%` }}></div>
        </div>

        <div
          className="comments-box"
          dangerouslySetInnerHTML={{ __html: commentsHtml }}
        ></div>
      </main>

      <footer className="footer">
        &copy; 2025 QUBUHUB — Built by Kubu Lee and powered by a constellation of ideas:<br />
        <a href="https://web4application.github.io/kubu-hai" target="_blank" rel="noreferrer">kubu-hai</a>,{" "}
        <a href="https://github.com/Web4application/fadaka" target="_blank" rel="noreferrer">Fadaka Blockchain</a>,{" "}
        <a href="https://github.com/Web4application/RODAAI" target="_blank" rel="noreferrer">RODAAI</a>,{" "}
        <a href="https://github.com/Web4application/Web4asset" target="_blank" rel="noreferrer">Web4Asset</a> and more.
      </footer>
    </div>
  );
};

export default Home;
