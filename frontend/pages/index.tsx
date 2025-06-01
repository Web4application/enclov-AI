// pages/index.tsx
import { useEffect, useState } from "react";

const API_ENDPOINT = "/api/comments"; // Change this to your actual API URL

export default function Home() {
  const [progress, setProgress] = useState(0);
  const [commentsHTML, setCommentsHTML] = useState(
    "🔄 Waiting for review..."
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [darkMode, setDarkMode] = useState(true);

  useEffect(() => {
    let interval: NodeJS.Timeout;

    async function fetchComments() {
      setLoading(true);
      setError(null);
      try {
        const res = await fetch(`${API_ENDPOINT}?job_id=12345`);
        if (!res.ok) throw new Error("Network response was not ok");
        const data = await res.json();
        setCommentsHTML(data.comments_html);
      } catch (e: any) {
        setError("❌ Failed to load comments.");
        console.error(e);
      } finally {
        setLoading(false);
      }
    }

    function simulateProgress() {
      interval = setInterval(() => {
        setProgress((prev) => {
          const next = prev + Math.random() * 10;
          if (next >= 100) {
            clearInterval(interval);
            fetchComments();
            return 100;
          }
          return next;
        });
      }, 600);
    }

    simulateProgress();

    return () => clearInterval(interval);
  }, []);

  return (
    <div className={`${darkMode ? "bg-gray-900 text-green-400" : "bg-white text-gray-900"} min-h-screen flex flex-col p-8 font-sans transition-colors duration-500`}>
      {/* Header with brand and dark mode toggle */}
      <header className="flex justify-between items-center mb-8">
        <h1 className="text-4xl font-bold tracking-wide drop-shadow-md">QUBUHUB</h1>
        <button
          onClick={() => setDarkMode(!darkMode)}
          className="px-4 py-2 bg-green-600 rounded hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500"
          aria-label="Toggle dark mode"
        >
          {darkMode ? "Light Mode" : "Dark Mode"}
        </button>
      </header>

      {/* Navigation menu */}
      <nav className="mb-8 flex space-x-6 text-lg">
        {["Home", "Projects", "AI Reviews", "About Us", "Contact"].map((item) => (
          <a
            key={item}
            href={`#${item.toLowerCase().replace(/\s+/g, "")}`}
            className="hover:underline cursor-pointer"
          >
            {item}
          </a>
        ))}
      </nav>

      {/* Intro / Company section */}
      <section id="home" className="mb-8 max-w-3xl">
        <p className="text-lg mb-4">
          Welcome to <strong>QUBUHUB</strong> — where innovation meets tradition in AI, blockchain, and web applications. Founded by Kubu Lee, our projects are the backbone of next-gen tech solutions:
        </p>
        <ul className="list-disc list-inside space-y-1 text-green-300">
          <li><a href="https://github.com/Web4application/enclov-AI" className="underline" target="_blank" rel="noreferrer">enclov-AI</a>: AI-powered GitHub PR code reviewer</li>
          <li><a href="https://github.com/Web4application/fadaka" className="underline" target="_blank" rel="noreferrer">Fadaka Blockchain</a>: Decentralized finance reinvented</li>
          <li><a href="https://github.com/Web4application/Lola" className="underline" target="_blank" rel="noreferrer">Lola</a>: AI personal assistant and creative muse</li>
          <li><a href="https://web4application.github.io/kubu-hai" className="underline" target="_blank" rel="noreferrer">Kubu-Hai</a>: The powerful AI webapp blockchain ecosystem</li>
        </ul>
      </section>

      {/* AI Review UI */}
      <section id="aireviews" className="mb-8 max-w-3xl w-full">
        <h2 className="text-3xl font-semibold mb-4">enclov-AI — GitHub PR Code Reviewer</h2>
        <p className="mb-4 max-w-xl text-gray-300">
          Supercharge your GitHub PR workflow with real-time AI-driven review automation. Powered by OpenAI, FastAPI, Redis, and Celery.
        </p>

        {/* Progress bar */}
        <div className="w-full bg-gray-800 rounded h-5 mb-4 overflow-hidden">
          <div
            className="bg-green-500 h-full transition-all duration-300"
            style={{ width: `${progress}%` }}
            aria-valuenow={progress}
            aria-valuemin={0}
            aria-valuemax={100}
            role="progressbar"
          />
        </div>

        {/* Comments Box */}
        <div
          className="bg-gray-800 p-4 rounded border-l-4 border-green-500 min-h-[150px] overflow-auto whitespace-pre-wrap"
          aria-live="polite"
          aria-atomic="true"
        >
          {loading ? "🔄 Loading AI review comments..." : error ? error : <span dangerouslySetInnerHTML={{ __html: commentsHTML }} />}
        </div>

        {/* GitHub link */}
        <a
          href="https://github.com/Web4application/enclov-AI"
          target="_blank"
          rel="noopener noreferrer"
          className="inline-block mt-6 px-6 py-2 bg-green-600 rounded hover:bg-green-700 text-white font-semibold transition-colors"
        >
          View on GitHub
        </a>
      </section>

      {/* Footer */}
      <footer className="mt-auto text-center text-gray-500 text-sm py-4 border-t border-gray-700">
        &copy; 2025 QUBUHUB by Kubu Lee. Built with containers, code, and conviction.
      </footer>
    </div>
  );
}
