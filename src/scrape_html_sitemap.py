import requests
from bs4 import BeautifulSoup
import json
import os

# CONFIGURATION
SITEMAP_URL = "https://www.shl.com/company/site-map/"
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "raw_assessments.json")

# Ensure output directory exists
os.makedirs(OUTPUT_DIR, exist_ok=True)

def scrape_html_sitemap():
    print(f"[INFO] Fetching HTML Sitemap: {SITEMAP_URL}")
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    try:
        response = requests.get(SITEMAP_URL, headers=headers, timeout=15)
        if response.status_code != 200:
            print(f"[ERROR] Failed to fetch page. Status: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, "html.parser")
        
        # We are looking for ANY link that goes to the product catalog
        product_links = set()
        
        # Iterate over all 'a' tags
        for a_tag in soup.find_all("a", href=True):
            href = a_tag['href']
            
            # The Golden Pattern
            if "/product-catalog/view/" in href:
                # Filter out "Job Focused" / "Pre-packaged" if needed
                if "job-focused" in href: 
                    continue 

                # Normalize URL
                full_link = href if href.startswith("http") else f"https://www.shl.com{href}"
                product_links.add(full_link)

        print(f"[INFO] Found {len(product_links)} unique product links.")
        
        if len(product_links) > 300:
            print("[SUCCESS] This sitemap is the key.")
            
            # Save strictly as a list of URLs first
            data = [{"url": url} for url in product_links]
            
            # We save to a temporary file so we don't overwrite any good data yet
            with open(os.path.join(OUTPUT_DIR, "sitemap_urls.json"), "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            print("[INFO] Saved URLs to 'data/sitemap_urls.json'")
            
        else:
            print(f"[WARN] Count is too low ({len(product_links)}). This might just be a section of the site.")

    except Exception as e:
        print(f"[ERROR] Error: {e}")

if __name__ == "__main__":
    scrape_html_sitemap()