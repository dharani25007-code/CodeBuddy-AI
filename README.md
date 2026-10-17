<div align="center">
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:0f1117,50:7C3AED,100:00ffe0&height=200&section=header&text=Zanaks%20AI&fontSize=52&fontColor=ffffff&fontAlignY=40&desc=Next-Gen%20Full-Stack%20AI%20Coding%20Studio%20(React%20%2B%20Python)&descAlignY=60&descSize=18&animation=fadeIn"/>
</div>

<div align="center">

![React 18](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react&logoColor=black)
![Vite](https://img.shields.io/badge/Vite-5.0-646CFF?style=for-the-badge&logo=vite&logoColor=white)
![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0%2B-000000?style=for-the-badge&logo=flask&logoColor=white)
![Supabase](https://img.shields.io/badge/PostgreSQL-Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-Local%20Dev-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local%20AI-FF6F00?style=for-the-badge&logo=ollama&logoColor=white)
![Socket.IO](https://img.shields.io/badge/Socket.IO-4.0%2B-010101?style=for-the-badge&logo=socket.io&logoColor=white)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](LICENSE)

> ⚡ **28 World-First AI Features · Modern React 18 Frontend · Clean Modular Backend · Zero-Cost Local AI**

</div>

---

## 🏛️ Clean Project Architecture

Zanaks AI is organized into clean, dedicated tiers: a **React 18 Frontend** with an ultra-modern cybernetic aerospace design system and a **Modular Python Backend** that powers the 28 World-First AI capabilities, WebSocket collaboration rooms, and zero-cost local LLM execution.

```
Zanaks AI/
├── backend/                         # 🐍 Python API & AI Services
│   ├── app.py                       # Main Flask & SocketIO application server
│   ├── run_backend.bat              # Direct Windows launcher for backend
│   ├── requirements.txt             # Backend dependencies (Flask, Flask-CORS, Bcrypt)
│   ├── gunicorn.conf.py             # Production Gunicorn WSGI configuration
│   ├── Procfile                     # Cloud deployment configuration
│   ├── generate_patent_pdf.py       # Patent feasibility matrix report generator
│   ├── appcore/                     # Database engine & connection pooling
│   │   ├── __init__.py
│   │   └── db.py                    # Transparent SQLite / PostgreSQL switcher
│   └── voice_profiles/              # Voice clone & TTS model cache
│
├── frontend/                        # ⚛️ React 18 & Vite Frontend Studio
│   ├── package.json                 # React 18, Vite, Lucide dependencies
│   ├── vite.config.js               # Dev server configuration with API proxy (port 3000)
│   ├── index.html                   # HTML5 application shell & Google Fonts
│   ├── standalone.html              # Zero-install browser-runnable React preview
│   ├── public/                      # Static assets, SVG favicons, manifests
│   │   └── favicon.svg              # 3D beveled aerospace Zanaks AI vector icon
│   └── src/
│       ├── main.jsx                 # React DOM mount entrypoint
│       ├── App.jsx                  # Main application & routing coordinator
│       ├── index.css                # Futuristic design system tokens, animations, scrollbars
│       ├── context/
│       │   ├── AuthContext.jsx      # Authentication state, guest login, streaks, karma
│       │   └── ThemeContext.jsx     # Dark Plasma Void & Cyberpunk Light mode switcher
│       ├── services/
│       │   └── api.js               # Universal API client for chat, code runner, & AI features
│       └── components/
│           ├── Navbar.jsx           # Top navigation, model selector, streak fire, karma badge
│           ├── Sidebar.jsx          # Conversation history, pin/rename/delete, workspace tabs
│           ├── ChatView.jsx         # AI chat feed, Thought Replay drawer, code copy & run
│           ├── CodeRunnerView.jsx   # Multi-language code editor (15+ langs) & Big-O complexity
│           ├── WorldFirstSuite.jsx  # Interactive showcase for all 28 World-First capabilities
│           ├── CollabView.jsx       # Real-time multi-user coding room & WebSocket chat
│           ├── LeaderboardView.jsx  # Global developer rankings & daily streak cards
│           ├── AuthModal.jsx        # Glassmorphic modal for Sign In, Sign Up, & Guest access
│           ├── SettingsModal.jsx    # Assistant persona tuning & custom system memory
│           └── VoiceModal.jsx       # Hands-free speech-to-speech coding loop
│
├── run.bat                          # 🚀 Master interactive launcher
├── run_all.bat                      # 🚀 One-click full-stack launcher (Backend + Frontend)
├── run_backend.bat                  # 🚀 Launches backend server on port 5000
├── run_frontend.bat                 # 🚀 Launches React frontend on port 3000
└── codebuddy.db                     # 💾 SQLite database (users, chats, karma, stats)
```

---

## 🚀 Quickstart Guide

### 1. Launch Everything in One Click
Double-click **`run.bat`** in the project folder, or run:
```cmd
run.bat
```
This presents an interactive menu:
- `[1]` Start Full Stack (Backend + React Frontend)
- `[2]` Start Python Backend Server (Port 5000)
- `[3]` Start React Frontend Dev Server (Port 3000)
- `[4]` Open React 18 Standalone Preview in Browser

### 2. Manual Commands

#### Python Backend:
```bash
cd backend
pip install -r requirements.txt
python app.py
```
Backend will be available at: `http://127.0.0.1:5000` (Health check: `http://127.0.0.1:5000/api/health`)

#### React Frontend:
```bash
cd frontend
npm install
npm run dev
```
Frontend will be available at: `http://localhost:3000`

---

## ✨ 28 World-First AI Capabilities

Zanaks AI introduces 28 groundbreaking features designed for modern software engineers:

1. **Error Autopsy (#26)**: Probabilistic root-cause ranking + visual diagnosis tree before fixing code.
2. **Pair Naming Assistant (#27)**: Name quality scoring + reverse body check: does this variable/function name match its implementation?
3. **Focus Zone Detector (#28)**: Session timestamp analytics revealing when you code with the highest flow and lowest error rate.
4. **Bug Prophecy Engine (#20)**: Predicts runtime crashes, null pointer exceptions, and race conditions before you compile.
5. **Code DNA Fingerprinting (#19)**: Identifies your personal coding style vector and formats AI output to match it.
6. **Dead Code Archaeologist (#18)**: AST parser that pinpoints uncalled methods, orphaned variables, and dead branches.
7. **Cognitive Load Scorer (#22)**: Evaluates mental complexity rating & nested branch fatigue vector for human readability.
8. **Thought Replay Debugger (#11)**: Streams the AI's internal step-by-step reasoning tree into an animated timeline.
9. **Voice-to-Voice Coding Loop (#12)**: Speak your code problem verbally → hear the diagnosed fix spoken back.
10. **Rubber Duck+ Mode (#23)**: Socratic AI mentor that deliberately refuses direct code solutions, prompting you with guided questions.
11. **Code Mood Engine (#17)**: Detects developer frustration and adapts empathy, patience, and restorative tips.
12. **Live Code Battle Arena (#13)**: Real-time 1v1 coding challenges with automated AI judging.
13. **Code Karma System (#14)**: Peer review points, contribution badges, and rank progression.
14. **Personal Changelog (#24)**: Auto-generated daily learning diary extracted from your sessions.
15. **Confidence Calibrator (#25)**: Validates AI code suggestions against test cases and known edge risks.
16. **Blind Code Review (#16)**: Anonymous code posting queue for objective peer grading.
17. **Time Machine (#21)**: Seamlessly revert and inspect chronological revisions of any snippet.
18. **Roadmap Generator**: Structured career and skill learning paths generated on demand.

---

## 🎨 Design Philosophy & Technology Stack

- **Theme Palette**: Dark Plasma Void (`#020408`), Deep Navy (`#060d1a`), Plasma Cyan (`#00ffe0`), Nova Purple (`#a855f7`), Fire Orange (`#ff6b2b`), Gold (`#fbbf24`).
- **Typography**: `IBM Plex Mono` for code blocks, metrics, and memory tokens; `Inter` for clean modern interfaces.
- **Micro-Animations**: Pulse glow accents, glassmorphic cards, custom cybernetic scrollbars.
- **Zero-Cost Engine**: Runs offline with local Ollama models (`qwen2.5-coder:7b`, `llama3.2:3b`) with free cloud fallbacks to Groq and OpenRouter.

---

## 📄 License

MIT License. Copyright © 2026 Dharanidharan M. All Rights Reserved.
#   Z a n a k s - A I  
 