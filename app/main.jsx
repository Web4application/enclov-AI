import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './src/App'

ReactDOM.createRoot(document.getElementById('root')).render(<App />)
document.getElementById("prForm").addEventListener("submit", async (e) => {
  e.preventDefault();
  const repoUrl = document.getElementById("repoUrl").value;
  const prNumber = document.getElementById("prNumber").value;
  commentBox.innerHTML = "⏳ Submitting PR for review...";

  try {
    const res = await fetch("/api/submit", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ repo_url: repoUrl, pr_number: parseInt(prNumber) })
    });
    const data = await res.json();
    if (data.job_id) {
      commentBox.innerHTML = "🚀 Review submitted successfully. Reviewing in progress...";
      pollStatus(data.job_id);
    } else {
      commentBox.innerHTML = "❌ Submission failed.";
    }
  } catch (err) {
    console.error(err);
    commentBox.innerHTML = "❌ Error submitting PR.";
  }
});

async function pollStatus(jobId) {
  const interval = setInterval(async () => {
    const res = await fetch(`/api/status/${jobId}`);
    const data = await res.json();
    if (data.status === "completed") {
      clearInterval(interval);
      commentBox.innerHTML = `<strong>AI Review Comments:</strong><br><br>${data.result.comments.join("<br>")}`;
    } else if (data.status === "failed") {
      clearInterval(interval);
      commentBox.innerHTML = `❌ Review failed: ${data.error}`;
    } else {
      commentBox.innerHTML = `<em>Analyzing diffs... (${data.status})</em>`;
    }
  }, 2000);
}
