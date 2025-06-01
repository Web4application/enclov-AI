import React, { useEffect, useState } from "react";

const styles = {
  body: {
    fontFamily: "'Segoe UI', Tahoma, sans-serif",
    background: "#0d0d0d",
    color: "#e0e0e0",
    minHeight: "100vh",
    display: "flex",
    flexDirection: "column",
    margin: 0,
    padding: 0,
  },
  header: {
    background: "#1a1a1a",
    padding: "1rem 2rem",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    borderBottom: "1px solid #333",
  },
  logo: {
    fontSize: "1.8rem",
    fontWeight: "bold",
    color: "#4caf50",
    textShadow: "0 0 4px #4caf50aa",
  },
  navLink: {
    color: "#ccc",
    marginLeft: "1.2rem",
    textDecoration: "none",
    fontSize: "1rem",
    transition: "0.3s ease",
  },
  navLinkHover: {
    color: "#4caf50",
  },
  main: {
    padding: "2rem",
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    flexGrow: 1,
  },
  h1: {
    color: "#4caf50",
    fontSize: "3rem",
    marginBottom: "0.5em",
    textShadow: "0 0 6px #4caf50cc",
  },
  lead: {
    fontSize: "1.3rem",
    maxWidth: "600px",
    textAlign: "center",
    color: "#bdbdbd",
  },
  button: {
    marginTop: "2rem",
    background: "#4caf50",
    color: "white",
    padding: "0.8em 1.6em",
    border: "none",
    borderRadius: "5px",
    fontSize: "1rem",
    cursor: "pointer",
    transition: "0.3s ease",
    textDecoration: "none",
    display: "inline-block",
  },
  buttonHover: {
    background: "#43a047",
  },
  progressContainer: {
    marginTop: "3rem",
    width: "100%",
    maxWidth: "600px",
    background: "#1e1e1e",
    borderRadius: "6px",
    overflow: "hidden",
  },
  progressBar: {
    height: "20px",
    background: "#4caf50",
    width: "0%",
    transition: "width 0.4s ease",
  },
  commentsBox: {
    marginTop: "3rem",
    background: "#1a1a1a",
    borderLeft: "4px solid #4caf50",
    padding: "1rem",
    maxWidth: "600px",
    borderRadius: "6px",
    fontSize: "0.95rem",
    whiteSpace: "pre-wrap",
  },
  footer: {
    marginTop: "auto",
    fontSize: "0.8rem",
    color: "#666",
    textAlign: "center",
    padding: "2rem",
  },
  projects: {
    marginTop: "4rem",
    maxWidth: "800px",
    textAlign: "left",
  },
  projectsH2: {
    color: "#4caf50",
    marginBottom: "1rem",
  },
  projectsUl: {
    paddingLeft: "1.2rem",
  },
  projectsLi: {
    marginBottom: "1rem",
  },
  projectsLink: {
    color: "#81d4fa",
  },
};

export default function EnclovAIPage() {
  const [progress, setProgress] = useState(0);
  const [comments, setComments] = useState("🔄 Waiting for review...");

  useEffect(() => {
    let interval;
    if (progress < 100) {
      interval = setInterval(() => {
        setProgress((prev) => {
          const next = prev + Math.random() * 10;
          if (next >= 100) {
            clearInterval(interval);
            setComments(
              `✅ Refactored inefficient loop at utils/helpers.py:45.\n` +
              `🛡️ Suggested stronger typing in main.py.\n` +
              `🧹 Unused imports cleaned in api/views.py.\n` +
              `🔒 Security note: avoid exposing tokens in logs.\n`
            );
            return 100;
          } else {
            setComments(`🔄 Analyzing diffs... (${Math.floor(next)}%)`);
            return next;
          }
        });
      }, 600);
    }
    return () => clearInterval(interval);
  }, [progress]);

  return (
    <div style={styles.body}>
      <header style={styles.header}>
        <div style={styles.logo}>QUBUHUB</div>
        <nav>
          <a href="#about" style={styles.navLink}>About</a>
          <a href="#projects" style={styles.navLink}>Projects</a>
          <a
            href="https://web4application.github.io/kubu-hai"
            target="_blank"
            rel="noopener noreferrer"
            style={styles.navLink}
          >
            Kubu-Hai
          </a>
          <a
            href="https://github.com/Web4application/enclov-AI"
            target="_blank"
            rel="noopener noreferrer"
            style={styles.navLink}
          >
            GitHub
          </a>
        </nav>
      </header>

      <main style={styles.main}>
        <h1 style={styles.h1}>enclov-AI</h1>
        <p style={styles.lead}>
          Supercharge your GitHub PR workflow with real-time AI-driven review automation. Powered by OpenAI, FastAPI, Redis, and Celery.
        </p>

        <a
          href="https://github.com/Web4application/enclov-AI"
          target="_blank"
          rel="noopener noreferrer"
          style={styles.button}
        >
          View on GitHub
        </a>

        <div style={styles.progressContainer}>
          <div
            style={{ ...styles.progressBar, width: `${Math.min(progress, 100)}%` }}
          />
        </div>

        <div style={styles.commentsBox}>{comments}</div>

        <section id="about" style={styles.projects}>
          <h2 style={styles.projectsH2}>🔍 About QUBUHUB</h2>
          <p>
            <strong>QUBUHUB</strong> is the heartbeat of next-gen open innovation. From soulful companions like <em>Lola</em> to decentralized infrastructure with <em>Fadaka</em>, we've been crafting the future, one stack at a time. Built by dreamers, hackers, and pragmatists.
          </p>
        </section>

        <section id="projects" style={styles.projects}>
          <h2 style={styles.projectsH2}>🚀 Projects from QUBUHUB</h2>
          <ul style={styles.projectsUl}>
            <li style={styles.projectsLi}>
              <strong>Lola</strong>: Emotionally intelligent AI companion.{" "}
              <a
                href="https://github.com/Web4application/Lola.git"
                target="_blank"
                rel="noopener noreferrer"
                style={styles.projectsLink}
              >
                GitHub
              </a>
            </li>
            <li style={styles.projectsLi}>
              <strong>RODAAI</strong>: Open-source AI + data science orchestration.{" "}
              <a
                href="https://github.com/Web4application/Web4AI_Project_Assistant.git"
                target="_blank"
                rel="noopener noreferrer"
                style={styles.projectsLink}
              >
                GitHub
              </a>
            </li>
            <li style={styles.projectsLi}>
              <strong>Fadaka Blockchain</strong>: Secure and extensible blockchain network.{" "}
              <a
                href="https://github.com/Web4application/fadaka.git"
                target="_blank"
                rel="noopener noreferrer"
                style={styles.projectsLink}
              >
                GitHub
              </a>
            </li>
            <li style={styles.projectsLi}>
              <strong>AgbakoAI</strong>: Adaptable modular AI for real-world industries.{" "}
              <a
                href="https://github.com/Web4application/agbakoAI"
                target="_blank"
                rel="noopener noreferrer"
                style={styles.projectsLink}
              >
                GitHub
              </a>
            </li>
            <li style={styles.projectsLi}>
              <strong>Swiftbot</strong>: Fast orchestration bot for modern workflows.{" "}
              <a
                href="https://github.com/Web4application/swiftbot.git"
                target="_blank"
                rel="noopener noreferrer"
                style={styles.projectsLink}
              >
                GitHub
              </a>
            </li>
            <li style={styles.projectsLi}>
              <strong>Kubu-Hai</strong>: Full-stack generator with FastAPI + Dart.{" "}
              <a
                href="https://github.com/Web4application/kubu-hai"
                target="_blank"
                rel="noopener noreferrer"
                style={styles.projectsLink}
              >
                GitHub
              </a>
            </li>
            <li style={styles.projectsLi}>
              <strong>Enclov-AI</strong>: The AI code reviewer you're reading right now.{" "}
              <a
                href="https://github.com/Web4application/enclov-AI"
                target="_blank"
                rel="noopener noreferrer"
                style={styles.projectsLink}
              >
                GitHub
              </a>
            </li>
          </ul>
        </section>
      </main>

      <footer style={styles.footer}>
        &copy; 2025 QUBUHUB. Built by Kubu Lee with containers, code, and conviction.
      </footer>
    </div>
  );
}
