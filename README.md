# enclov-AI

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Build Status](https://github.com/Web4application/enclov-AI/actions/workflows/docker-ci.yml/badge.svg)](https://github.com/Web4application/enclov-AI/actions)

---

![enclov-AI Banner](./docs/assets/enclov-ai-banner.png)

**Automated AI-Powered GitHub Pull Request Reviewer**

Enclov-AI seamlessly integrates with GitHub as a webhook-powered AI assistant that analyzes pull request diffs and generates insightful code reviews, leveraging OpenAI's GPT models.

---

## 🚀 Features

- **Webhook Listener:** Real-time pull request event handling from GitHub.
- **Secure Verification:** HMAC SHA-256 signature validation for payload security.
- **GitHub App Authentication:** JWT-based authentication for API access.
- **AI-Powered Review:** Uses OpenAI GPT-4o-mini to produce contextual PR feedback.
- **Automated Comments:** Posts review comments directly on GitHub PRs.
- **Docker & CI/CD:** Ready for containerized deployment and continuous integration.

---

## 📸 Demo

![Webhook Flow](./docs/assets/webhook-flow.png)

*Illustration of webhook event flow and AI review posting.*

---

## 🛠️ Installation

### Prerequisites

- Python 3.10 or newer
- Docker (optional)
- GitHub App with configured webhook secret and private key
- OpenAI API key

### Setup Environment Variables

Create a `.env` file in your project root:

```env
GITHUB_WEBHOOK_SECRET=your_webhook_secret_here
GITHUB_APP_ID=your_github_app_id_here
GITHUB_PRIVATE_KEY_PATH=/path/to/private-key.pem
OPENAI_API_KEY=your_openai_api_key_here
