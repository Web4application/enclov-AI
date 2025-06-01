// pages/api/comments.ts
import type { NextApiRequest, NextApiResponse } from "next";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const { job_id } = req.query;

  // Simulated AI comments HTML
  const comments_html = `
    <ul style="padding-left:1.2rem; margin:0;">
      <li>✅ <strong>Refactored</strong> inefficient loop at <code>utils/helpers.py:45</code>.</li>
      <li>🛡️ <strong>Suggested</strong> stronger typing in <code>main.py</code>.</li>
      <li>🧹 <strong>Removed</strong> unused imports in <code>api/views.py</code>.</li>
      <li>🔒 <strong>Security note:</strong> avoid exposing tokens in logs.</li>
    </ul>
  `;

  res.status(200).json({ comments_html, job_id });
}
