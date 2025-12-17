# 🏆 Intelligent Assessment Recommendation Engine

![Python](https://img.shields.io/badge/Python-3.8%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white)
![AWS](https://img.shields.io/badge/AWS_EC2-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white)

An **AI-powered Full Stack application** designed to recommend the best hiring assessments based on job descriptions or skill queries.  
It utilizes a **Hybrid Search Architecture (Semantic + Keyword)** to ensure high relevance and recall, and is fully deployed on **AWS EC2**.

---

## 📖 Table of Contents
- Architecture
- Key Features
- Tech Stack
- Installation & Local Setup
- AWS Deployment & Network Security
- API Documentation
- Project Structure
- Contact & License

---

## 🏗 Architecture

```mermaid
graph TD
    User[User / Recruiter] -->|HTTP Request| UI[Streamlit Frontend :8501]
    UI -->|POST JSON Payload| API[Flask API :8000]
    subgraph Backend Engine
        API -->|Query Processing| Logic[Grandmaster Logic]
        Logic -->|Semantic Search| FAISS[(FAISS Vector DB)]
        Logic -->|Keyword Matching| Filter[Keyword Bonus Algorithm]
        FAISS -->|Embeddings| HF[HuggingFace MiniLM]
    end
    Logic -->|Ranked Recommendations| UI
```

---

## 🌟 Key Features

- Hybrid Semantic + Keyword search
- FAISS-based high-speed retrieval
- Decoupled frontend and backend
- Production deployment on AWS EC2
- Smart assessment filtering

---

## 🛠 Tech Stack

| Component | Technology |
|--------|------------|
| Frontend | Streamlit |
| Backend | Flask |
| AI Model | HuggingFace MiniLM |
| Vector DB | FAISS |
| Deployment | AWS EC2 |
| Server | Gunicorn |

---

## 🚀 Installation & Local Setup

```bash
git clone https://github.com/your-username/Assessment-Recommendation-Engine.git
cd Assessment-Recommendation-Engine
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
streamlit run frontend.py
```

---

## ☁️ AWS Deployment & Network Security

| Port | Usage |
|----|------|
| 8501 | Streamlit UI |
| 8000 | Flask API |
| 22 | SSH |
| 80 | HTTP |

---

## 🔌 API Documentation

### Health Check
GET /health

```json
{ "status": "healthy" }
```

### Recommendation API
POST /recommend

```json
{ "query": "Java Developer with SQL skills" }
```

---

## 📂 Project Structure

```bash
Assessment-Recommendation-Engine/
├── data/
├── app.py
├── frontend.py
├── requirements.txt
├── README.md
└── submission.csv
```

---

## 📧 Contact & License

Developer: Your Name  
License: MIT  
Status: ✅ Completed & Deployed
