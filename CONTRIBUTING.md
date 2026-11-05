# Contributing to Auth_forge

Thank you for your interest in contributing to **Auth_forge**! We welcome contributions ranging from bug fixes and documentation improvements to new security features and frontend enhancements.

---

## Getting Started

1. **Fork the repository** on GitHub.
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/<your-username>/Auth_forge.git
   cd Auth_forge
   ```
3. **Create a new branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bugfix-name
   ```

---

## Local Development Setup

### Backend (FastAPI)
1. Set up a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Copy environment configuration:
   ```bash
   cp .env.example .env   # On Windows: copy .env.example .env
   ```
4. Start the backend:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

### Frontend (React + Vite)
1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```
2. Install dependencies:
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

---

## Development Guidelines

- **Code Style**:
  - Python code should adhere to PEP 8 conventions with clean type hints where appropriate.
  - Frontend code should pass Oxlint checks (`npm run lint` in the `frontend` folder).
- **Security-First Mindset**:
  - Never commit raw passwords, tokens, or live production secrets to git.
  - Keep sensitive data stored in `.env` (ignored by git).
  - Ensure password hashes are generated using Argon2 / recommended password hashing providers.
- **Commit Messages**:
  - Use clear, descriptive commit messages following conventional commits:
    - `feat: add user profile picture upload`
    - `fix: resolve token expiry check on refresh`
    - `docs: update API endpoints in README`

---

## Submitting Pull Requests

1. Push your branch to your forked repository:
   ```bash
   git push origin feature/your-feature-name
   ```
2. Open a Pull Request against the `main` branch.
3. Fill in the PR description explaining:
   - The rationale behind the changes.
   - Any manual or automated tests conducted.
   - Any breaking changes or schema migrations.
4. Respond to feedback during code review.
