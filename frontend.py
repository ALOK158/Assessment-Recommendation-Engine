# Usage: streamlit run frontend.py
import streamlit as st
import requests

# CONFIGURATION
# ⚠️ REPLACE THIS WITH YOUR PUBLIC API URL AFTER DEPLOYING STEP 3
API_URL = "http://localhost:5000/recommend" 

st.set_page_config(page_title="SHL Recommender", page_icon="🎯")
st.title("🎯 SHL Assessment Recommender")
st.markdown("Enter a job description or skill requirement below.")

# Input
query = st.text_area("Job Requirement:", "Need a Java Developer with Team Lead experience.")

if st.button("Find Assessments"):
    if not query:
        st.warning("Please enter a query.")
    else:
        with st.spinner("Searching Catalog..."):
            try:
                response = requests.post(API_URL, json={"query": query})
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("recommended_assessments", [])
                    st.success(f"Found {len(results)} matches!")
                    
                    for item in results:
                        with st.expander(f"📄 {item['name']}"):
                            st.write(f"**Types:** {', '.join(item['test_type'])}")
                            st.write(f"**Duration:** {item['duration']} mins")
                            st.write(f"**Description:** {item['description']}")
                            st.markdown(f"🔗 [View Assessment]({item['url']})")
                else:
                    st.error(f"API Error: {response.status_code}")
            except Exception as e:
                st.error(f"Connection Failed: {e}. Is the API running?")