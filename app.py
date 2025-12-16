# =============================================================================
# 🏆 SHL AI ASSESSMENT - FLASK API (APPENDIX 2 COMPLIANT)
# =============================================================================
# Usage: python app.py

import os
import json
import re
from flask import Flask, request, jsonify
from flask_cors import CORS
from langchain_core.documents import Document
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

app = Flask(__name__)
CORS(app)  # Allow frontend to access API

# ---------------------------------------------------------
# 1. LOAD ENGINE (Your Optimized Logic)
# ---------------------------------------------------------
print("🔧 Initializing API...")
# Change this line in app.py to point to the data subfolder
DATA_PATH = "data/raw_assessments.json"  # Ensure this file is present

# Load Data
# Tell Python to use the universal web standard encoding
with open(DATA_PATH, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

documents = []
for item in raw_data:
    name = item.get('name', 'Unknown')
    test_types = item.get('test_type', [])
    
    # STRICT FILTERING 
    if "Pre-packaged Job Solutions" in test_types: continue
    if "Solution" in name and "Individual" not in str(test_types): continue

    # Create Document
    page_content = f"Title: {name} | Type: {', '.join(test_types)} | Desc: {item.get('description', '')}"
    
    # Tokenizer Logic
    text = page_content.lower()
    tokens = re.findall(r"\b[a-z][a-z0-9]*(?:[.+#][a-z0-9]+)*\+*", text)
    stopwords = {"hire", "hiring", "role", "junior", "senior", "developer", "engineer", "test", "assessment", "looking", "need"}
    doc_tokens = set(t for t in tokens if t not in stopwords and len(t) > 1)
    
    metadata = {
        "name": name,
        "url": item.get("url"),
        "adaptive_support": item.get("adaptive_support", "No"),
        "description": item.get("description", ""),
        "duration": item.get("duration"),
        "remote_support": item.get("remote_support", "Yes"),
        "test_type": test_types,
        "doc_tokens": list(doc_tokens)
    }
    documents.append(Document(page_content=page_content, metadata=metadata))

# Build Vector Index
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vector_db = FAISS.from_documents(documents, embeddings)
print("✅ API Ready & Index Built.")

# ---------------------------------------------------------
# 2. HELPER FUNCTIONS
# ---------------------------------------------------------
def clean_query(text):
    fluff = ["i am hiring for", "looking to hire", "i need a", "we are looking for"]
    cleaned = text.lower()
    for phrase in fluff: cleaned = cleaned.replace(phrase, "")
    return " ".join(cleaned.split())

def extract_tokens(text):
    tokens = re.findall(r"\b[a-z][a-z0-9]*(?:[.+#][a-z0-9]+)*\+*", text.lower())
    stopwords = {"hire", "hiring", "role", "junior", "senior", "developer", "engineer"}
    return set(t for t in tokens if t not in stopwords and len(t) > 1)

# ---------------------------------------------------------
# 3. ENDPOINTS (Strict Appendix 2 Spec)
# ---------------------------------------------------------

@app.route('/health', methods=['GET'])
def health_check():
    """
    Ref: Appendix 2, Page 6 
    """
    return jsonify({"status": "healthy"}), 200

@app.route('/recommend', methods=['POST'])
def recommend():
    """
    Ref: Appendix 2, Page 6 
    """
    try:
        data = request.get_json()
        if not data or 'query' not in data:
            return jsonify({"error": "Missing 'query' field"}), 400
        
        query = data['query']
        
        # Hybrid Search Logic
        opt_query = clean_query(query)
        query_skills = extract_tokens(query)
        num_q_skills = max(len(query_skills), 1)

        raw_results = vector_db.similarity_search_with_score(opt_query, k=30)
        scored_candidates = []
        
        for doc, distance in raw_results:
            v_score = 1 / (1 + distance)
            doc_skill_set = set(doc.metadata.get('doc_tokens', []))
            overlap = len(query_skills.intersection(doc_skill_set))
            skill_bonus = min(1.0, overlap / num_q_skills)
            
            final_score = (v_score * 0.7) + (skill_bonus * 0.3)
            scored_candidates.append((final_score, doc))
        
        scored_candidates.sort(key=lambda x: x[0], reverse=True)
        top_results = [d for _, d in scored_candidates][:10] # Max 10 

        # Response Format 
        response_list = []
        for doc in top_results:
            md = doc.metadata
            response_list.append({
                "url": md.get("url"),
                "name": md.get("name"),
                "adaptive_support": md.get("adaptive_support"), # CORRECTED
                "description": md.get("description"),
                "duration": md.get("duration"),
                "remote_support": md.get("remote_support"), # CORRECTED
                "test_type": md.get("test_type")
            })

        return jsonify({"recommended_assessments": response_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Run on port 5000 (Gunicorn will run on 8000)
    app.run(host='0.0.0.0', port=5000)