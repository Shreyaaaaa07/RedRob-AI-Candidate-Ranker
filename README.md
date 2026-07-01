# 🚀 RedRob AI Candidate Ranker

> **An AI-Powered Explainable Candidate Ranking Platform that intelligently evaluates, ranks, and analyzes candidates using semantic matching, hybrid scoring, recruiter intelligence, and explainable AI.**

<p align="center">

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688?logo=fastapi)
![React](https://img.shields.io/badge/React-Frontend-61DAFB?logo=react)
![Vite](https://img.shields.io/badge/Vite-Build-646CFF?logo=vite)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Engineering-150458?logo=pandas)
![Scikit Learn](https://img.shields.io/badge/Scikit--Learn-ML-F7931E?logo=scikitlearn)
![Render](https://img.shields.io/badge/Backend-Render-46E3B7)
![Vercel](https://img.shields.io/badge/Frontend-Vercel-black?logo=vercel)

</p>

---

## 🌐 Live Demo

### 🖥️ Frontend

**Live Application**

https://red-rob-ai-candidate-ranker.vercel.app/

---

### ⚙️ Backend API

https://redrob-ai-candidate-ranker.onrender.com

---

### 📚 Swagger API Documentation

https://redrob-ai-candidate-ranker.onrender.com/docs

---

# 📌 Project Overview

Recruiters receive hundreds or even thousands of resumes for a single job opening. Traditional Applicant Tracking Systems (ATS) primarily rely on keyword matching, often overlooking highly qualified candidates who may use different wording or possess transferable skills.

**RedRob AI Candidate Ranker** is an AI-powered recruitment intelligence platform that automates candidate evaluation using a hybrid scoring engine, semantic similarity, feature engineering, recruiter behavior signals, and explainable AI.

Instead of relying solely on keyword matching, the platform evaluates candidates across multiple dimensions including technical skills, experience consistency, production machine learning expertise, ranking system knowledge, vector database experience, behavioral indicators, and recruiter engagement metrics.

The system generates transparent rankings, identifies hiring risks, and provides evidence-based explanations to help recruiters make faster and more informed hiring decisions.

The application is built as a full-stack solution with a React frontend, FastAPI backend, AI-driven ranking pipeline, analytics dashboard, and REST APIs, making it suitable for modern AI-assisted recruitment workflows.

# ❗ Problem Statement

Hiring teams spend significant time manually reviewing resumes while existing Applicant Tracking Systems often depend heavily on keyword matching.

This leads to several challenges:

- Qualified candidates may be rejected because they use different terminology.
- Resume screening becomes slow and inefficient.
- Recruiters receive little explanation about why a candidate was recommended.
- Candidate ranking lacks transparency.
- Important hiring risks are difficult to identify manually.
- Traditional ATS systems rarely consider behavioral signals or recruiter engagement.

These limitations increase hiring time, reduce candidate quality, and make recruitment less efficient.

RedRob AI Candidate Ranker addresses these challenges by introducing an AI-powered explainable ranking engine capable of evaluating candidates using semantic understanding, feature engineering, recruiter intelligence, and transparent scoring.

# 💡 Solution

RedRob AI Candidate Ranker provides an intelligent end-to-end recruitment assistant that automatically evaluates and ranks candidates for a given job description.

The system performs:

- Job Description Parsing
- Candidate Feature Engineering
- Semantic Resume Matching
- Hybrid AI Candidate Ranking
- Risk Detection
- Explainable AI
- Recruiter Analytics
- Candidate Comparison
- Interactive Dashboard

Instead of relying on a single metric, the platform combines multiple evaluation dimensions into one hybrid score that better represents overall candidate suitability.

Recruiters receive:

- Ranked candidate lists
- Candidate insights
- Hiring recommendations
- Risk indicators
- Explainable evidence
- Analytics dashboard

allowing faster and more informed hiring decisions.

# ✨ Key Features

## 🤖 AI Candidate Ranking

- Hybrid AI Scoring Engine
- Semantic Resume Matching
- Skill Matching
- Experience Evaluation
- Recruiter Intelligence Signals

---

## 📊 Recruiter Dashboard

- Total Candidates
- Average Candidate Score
- Risk Analysis
- Top Ranked Candidates
- AI Insights

---

## 📈 Analytics Dashboard

- Score Distribution
- Candidate Statistics
- Risk Distribution
- Skill Analytics
- Recruiter Metrics

---

## 🔍 Explainable AI

Instead of only displaying a ranking score, the platform explains:

- Why a candidate ranked highly
- Missing skills
- Matching skills
- Resume evidence
- Semantic similarity
- Risk flags

---

## ⚠️ Risk Detection

Automatically detects:

- Employment gaps
- Low recruiter engagement
- Missing critical skills
- Career instability
- Resume inconsistencies

---

## 👤 Candidate Details

Each candidate profile displays:

- Hybrid Score
- Rank
- Feature Scores
- Evidence
- Risk Analysis
- Behavioral Signals

---

## 🔄 Candidate Comparison

Compare two candidates side-by-side using AI-generated feature scores and recruiter metrics.

# 🛠 Tech Stack

## Frontend

- React.js
- Vite
- React Router
- Axios
- Recharts
- Tailwind CSS

---

## Backend

- FastAPI
- Python
- REST APIs
- Pydantic

---

## AI & Machine Learning

- Pandas
- NumPy
- Scikit-Learn
- Semantic Similarity
- Hybrid Scoring
- Feature Engineering
- Explainable AI

---

## Data Processing

- Parquet
- JSON
- CSV

---

## Deployment

Frontend

- Vercel

Backend

- Render

---

## Development Tools

- Git
- GitHub
- VS Code
- Swagger UI

# 🏗️ System Architecture

The RedRob AI Candidate Ranker follows a modular full-stack architecture that combines AI-powered candidate evaluation with an interactive recruiter dashboard.

```text
                         ┌───────────────────────────┐
                         │     Job Description       │
                         └─────────────┬─────────────┘
                                       │
                                       ▼
                         ┌───────────────────────────┐
                         │   JD Parsing Engine        │
                         │ Extract Skills, Keywords   │
                         │ Experience, Education      │
                         └─────────────┬─────────────┘
                                       │
                                       ▼
                    ┌─────────────────────────────────────┐
                    │ Candidate Feature Engineering Engine │
                    └─────────────┬────────────────────────┘
                                  │
         ┌────────────────────────┼────────────────────────┐
         ▼                        ▼                        ▼
 Experience Match          Skill Match          Semantic Similarity
         │                        │                        │
         ├────────────────────────┼────────────────────────┤
         ▼                        ▼                        ▼
 Production ML      Vector DB Experience     Ranking Systems
         │                        │                        │
         ├────────────────────────┼────────────────────────┤
         ▼                        ▼                        ▼
 Startup Fit          Open Source Score     Education Score
         │                        │                        │
         ├────────────────────────┼────────────────────────┤
         ▼                        ▼                        ▼
 Career Stability      Recruiter Signals     Activity Score
                                  │
                                  ▼
                  ┌────────────────────────────────┐
                  │   Hybrid AI Ranking Engine      │
                  └──────────────┬─────────────────┘
                                 │
          ┌──────────────────────┼──────────────────────┐
          ▼                      ▼                      ▼
   Risk Detection        Explainable AI         Candidate Ranking
          │                      │                      │
          └──────────────┬───────┴──────────────────────┘
                         ▼
                Recruiter Dashboard
```

---

# 🔄 Complete Workflow

The system processes every candidate through multiple AI-powered stages before generating the final ranking.

---

## Step 1 — Job Description Parsing

The recruiter provides a Job Description.

The parser automatically extracts:

- Required Skills
- Preferred Skills
- Years of Experience
- Education Requirements
- AI Technologies
- Important Keywords
- Domain Knowledge

These extracted features become the benchmark against which every candidate is evaluated.

---

## Step 2 — Candidate Feature Engineering

Each candidate profile is transformed into structured numerical features.

Examples include:

- Experience Match
- Skill Match
- Semantic Similarity
- Production ML Experience
- Retrieval Systems
- Ranking Systems
- Vector Database Experience
- Startup Experience
- Open Source Contributions
- Education Score
- Recruiter Interest
- Activity Score
- Engagement Score
- Availability Score
- Career Stability
- Experience Consistency

These engineered features provide a comprehensive representation of every candidate.

---

## Step 3 — Semantic Resume Matching

Instead of relying only on keyword matching, the system measures the semantic similarity between the resume and the Job Description.

This enables the platform to recognize candidates who use different terminology while possessing equivalent skills and experience.

For example:

Resume:
> "Built embedding-based search systems."

Job Description:
> "Experience with vector databases and semantic retrieval."

Although the exact keywords differ, semantic matching recognizes their similarity.

---

## Step 4 — Hybrid AI Ranking

All engineered features are combined into a Hybrid Ranking Score.

Instead of using a single metric, the platform evaluates candidates across multiple dimensions including:

- Technical Skills
- Experience
- AI Knowledge
- Production Readiness
- Recruiter Signals
- Behavioral Metrics
- Risk Factors

The resulting Hybrid Score determines the final candidate ranking.

---

## Step 5 — Risk Detection

The platform automatically identifies potential hiring risks.

Examples include:

- Employment Gaps
- Career Instability
- Low Recruiter Engagement
- Missing Required Skills
- Resume Inconsistencies

Candidates with identified risks are highlighted for recruiter review.

---

## Step 6 — Explainable AI

Instead of presenting only a score, the system explains why a candidate achieved that ranking.

The explanation includes:

- Matched Skills
- Missing Skills
- Semantic Similarity
- Production Experience
- Ranking System Experience
- Vector Database Knowledge
- Career Stability
- Risk Flags

This provides complete transparency during the recruitment process.

---

## Step 7 — Recruiter Dashboard

The processed results are presented through an interactive dashboard containing:

- Candidate Rankings
- Analytics
- Candidate Details
- AI Insights
- Risk Statistics
- Score Distribution
- Top Candidates

Recruiters can efficiently evaluate candidates without manually reviewing every resume.

---

# 🧠 AI Feature Engineering Pipeline

The Feature Engineering Engine transforms raw candidate information into structured numerical features used by the ranking model.

## Engineered Features

| Feature | Description |
|----------|-------------|
| Experience Match | Compares candidate experience with job requirements |
| Skill Match | Measures overlap between required and candidate skills |
| Semantic Similarity | AI-based similarity between resume and job description |
| Production ML Score | Production-level Machine Learning experience |
| Retrieval Score | Search and Retrieval Systems expertise |
| Vector Database Score | Experience with embedding databases |
| Ranking System Score | Learning-to-Rank expertise |
| Evaluation Framework Score | A/B Testing and evaluation knowledge |
| Startup Fit | Startup experience and adaptability |
| Open Source Score | OSS contributions |
| Education Score | Academic qualification relevance |
| Career Stability | Employment consistency |
| Experience Consistency | Claimed vs actual experience |
| Recruiter Interest | Recruiter engagement signals |
| Activity Score | Candidate activity metrics |
| Engagement Score | Resume completeness |
| Availability Score | Availability for hiring |
| Behavior Score | Overall behavioral profile |
| Risk Score | Candidate risk evaluation |

These features collectively form the Hybrid Ranking Score used by the platform.

# 🤖 Hybrid AI Ranking Engine

The Hybrid Ranking Engine combines multiple candidate evaluation metrics into a single explainable ranking score.

Instead of relying solely on keyword matching, the engine considers:

- Technical Skills
- Practical Experience
- Semantic Similarity
- Production Readiness
- Behavioral Indicators
- Recruiter Signals
- Risk Analysis

This approach produces significantly more reliable candidate rankings compared to traditional Applicant Tracking Systems.

The ranking engine is designed to be transparent, explainable, and recruiter-friendly.

# 📊 Analytics Dashboard

The Analytics Dashboard provides recruiters with actionable insights into the candidate pool.

Instead of only displaying candidate rankings, the dashboard visualizes hiring trends and overall recruitment quality.

## Dashboard Metrics

- 📌 Total Candidates
- 📈 Average Hybrid Score
- 🏆 Top Candidate Score
- ⚠️ Risk Flagged Candidates

---

## 📉 Score Distribution

The platform groups candidates into score ranges to help recruiters understand the overall quality of applicants.

Example:

```
90-100 ████████████
80-89  █████████
70-79  ███████
60-69  █████
50-59  ███
Below 50 ██
```

This helps recruiters quickly understand how competitive the applicant pool is.

---

## 📌 Top Skills Analysis

The Analytics module also identifies the most common skills found among highly ranked candidates.

Examples include:

- Python
- Machine Learning
- FastAPI
- React
- SQL
- Vector Databases
- Retrieval Systems
- Ranking Systems
- Deep Learning
- NLP

This enables recruiters to identify important hiring trends.

---

## 🧠 AI Recruiter Insights

The platform automatically generates recruiter-friendly insights such as:

✔ 83 candidates are low risk.

✔ Average hybrid score is 72.4.

✔ 35 candidates scored above 80.

✔ Top candidate demonstrates strong semantic similarity and production ML experience.

These insights reduce manual analysis and accelerate hiring decisions.

# 📡 REST API

The backend exposes RESTful APIs developed using FastAPI.

| Method | Endpoint | Description |
|----------|----------------------|--------------------------------|
| GET | / | API Status |
| GET | /health | Health Check |
| GET | /dashboard | Dashboard Statistics |
| GET | /ranking | Candidate Rankings |
| GET | /candidate/{candidate_id} | Candidate Details |
| GET | /analytics | Analytics Dashboard |
| GET | /docs | Swagger Documentation |

---

## Example API Response

```json
{
    "candidate_id": "CAND_0000031",
    "hybrid_score": 71.39,
    "rank": 1,
    "risk_score": 0,
    "semantic_similarity_score": 0.67,
    "skill_match_score": 0.50
}
```

# 📂 Project Structure

```
RedRob-AI-Candidate-Ranker
│
├── backend
│   ├── app
│   │   ├── api
│   │   ├── services
│   │   ├── models
│   │   ├── config.py
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend
│   ├── src
│   │
│   ├── components
│   ├── hooks
│   ├── layouts
│   ├── pages
│   ├── services
│   ├── App.jsx
│   └── main.jsx
│
├── data
├── outputs
├── docs
├── README.md
└── requirements.txt
```

# 🚀 Installation

## Clone Repository

```bash
git clone https://github.com/<YOUR_USERNAME>/RedRob-AI-Candidate-Ranker.git

cd RedRob-AI-Candidate-Ranker
```

---

## Backend Setup

```bash
cd backend

python -m venv venv

source venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

Backend runs on

```
http://127.0.0.1:8000
```

---

## Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend runs on

```
http://localhost:5173
```


# ☁️ Deployment

## Frontend

Hosted on **Vercel**

🔗 https://red-rob-ai-candidate-git-e34d08-sharmashreya7676-2648s-projects.vercel.app

---

## Backend

Hosted on **Render**

🔗 https://redrob-ai-candidate-ranker.onrender.com

---

## API Documentation

FastAPI Swagger

🔗 https://redrob-ai-candidate-ranker.onrender.com/docs

# 📸 Application Screenshots

## 🏠 Recruiter Dashboard

![image alt](https://github.com/Shreyaaaaa07/RedRob-AI-Candidate-Ranker/blob/b71d619e8cb25569293784f4d36a15ff32eebc3b/Screenshot%202026-07-01%20212256.png)

---

## 📊 Candidate Rankings

![image alt](https://github.com/Shreyaaaaa07/RedRob-AI-Candidate-Ranker/blob/b71d619e8cb25569293784f4d36a15ff32eebc3b/Screenshot%202026-07-01%20212409.png)

---

## 👤 Candidate Details

![image alt](https://github.com/Shreyaaaaa07/RedRob-AI-Candidate-Ranker/blob/b71d619e8cb25569293784f4d36a15ff32eebc3b/Screenshot%202026-07-01%20212354.png)

---

## 📈 Analytics Dashboard

![image alt](https://github.com/Shreyaaaaa07/RedRob-AI-Candidate-Ranker/blob/b71d619e8cb25569293784f4d36a15ff32eebc3b/Screenshot%202026-07-01%20212446.png)
---


# 👥 Team Contributions

## 👨‍💻 Dev Shrivastava(Team Leader)

### Backend & AI Engineering

- FastAPI Backend Development
- AI Ranking Pipeline
- Feature Engineering
- Candidate Risk Detection
- Explainable AI
- Analytics APIs
- Deployment (Render)

---

## 👩‍💻 Shreya Sharma

### Frontend Engineering

- React Frontend
- Dashboard UI
- Candidate Ranking Interface
- Candidate Details
- Analytics Dashboard
- API Integration
- Deployment (Vercel)

# 🛣️ Future Enhancements

Future versions of the platform may include:

- 🤖 LLM-powered recruiter assistant
- 📄 Resume PDF upload
- 💬 AI-generated candidate summaries
- 🎤 Interview scheduling
- 📧 Email notifications
- 🔐 Authentication & Authorization
- 🗄 PostgreSQL integration
- ☁ AWS S3 storage
- 🐳 Docker support
- ☸ Kubernetes deployment
- 📱 Mobile responsive recruiter dashboard
- 📈 Real-time hiring analytics


# 🏆 Key Highlights

✅ Full Stack AI Application

✅ Explainable Candidate Ranking

✅ Hybrid AI Scoring Engine

✅ Semantic Resume Matching

✅ Recruiter Analytics Dashboard

✅ Candidate Risk Detection

✅ FastAPI REST APIs

✅ React + Vite Frontend

✅ Production Deployment (Render + Vercel)

✅ Modular Scalable Architecture

# 📜 License

This project was developed for educational purposes, portfolio demonstration, and hackathon participation.

Feel free to explore the codebase, learn from the implementation, and build upon the ideas while respecting the repository license.


# ⭐ Support

If you found this project useful or interesting:

⭐ Star the repository

🍴 Fork the project

💡 Share feedback and suggestions

Contributions, discussions, and improvements are always welcome.
