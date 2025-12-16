import requests
from bs4 import BeautifulSoup
import json
import time
import os
import random
import re
from urllib.parse import urljoin

# --- CONFIGURATION ---
BASE_URL = "https://www.shl.com/products/product-catalog/"
OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "raw_assessments.json")

os.makedirs(OUTPUT_DIR, exist_ok=True)

class SHLScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })
        self.assessments = []
        self.visited_urls = set()

        # THE ROSETTA STONE MAP (From your screenshot)
        self.type_map = {
            "A": "Ability & Aptitude",
            "B": "Biodata & Situational Judgement",
            "C": "Competencies",
            "D": "Development & 360",
            "E": "Assessment Exercises",
            "K": "Knowledge & Skills",
            "P": "Personality & Behavior",
            "S": "Simulations"
        }

    def get_soup(self, url):
        try:
            time.sleep(random.uniform(0.5, 1.2))
            response = self.session.get(url, timeout=20)
            if response.status_code == 200:
                return BeautifulSoup(response.content, "html.parser")
        except Exception as e:
            print(f"[ERROR] Failed to fetch {url}: {e}")
        return None

    def clean_text(self, text):
        if not text: return ""
        return " ".join(text.split())

    def crawl(self):
        print(f"[INFO] Starting Surgical Crawl...")
        step = 12
        max_start = 800 
        
        for start_index in range(0, max_start, step):
            if start_index == 0: url = BASE_URL
            else: url = f"{BASE_URL}?start={start_index}"
            
            page_num = (start_index // step) + 1
            print(f"[INFO] Scraping Page {page_num} (start={start_index})...")
            
            soup = self.get_soup(url)
            if not soup: break
            
            new_links_found = 0
            for a in soup.find_all("a", href=True):
                href = a['href']
                if "/product-catalog/view/" in href:
                    if "job-focused" in href: continue 
                    full_link = urljoin(BASE_URL, href)
                    if full_link not in self.visited_urls:
                        self.visited_urls.add(full_link)
                        self.scrape_product(full_link)
                        new_links_found += 1
            
            print(f"   + Found {new_links_found} new items. Total: {len(self.assessments)}")
            self.save()
            
            if new_links_found == 0 and start_index > 0:
                break

    def scrape_product(self, url):
        soup = self.get_soup(url)
        if not soup: return
        
        data = {
            "url": url,
            "name": "Unknown",
            "description": "",
            "duration": 0,
            "test_type": [],
            "adaptive_support": "No",
            "remote_support": "Yes"
        }
        
        try:
            # 1. NAME
            h1 = soup.find("h1")
            if h1: data["name"] = self.clean_text(h1.text)

            # 2. ISOLATE CONTENT
            main_content = soup.find("main") or soup.find("article") or soup.find("div", class_="product-detail-content")
            
            # Remove footer/nav trash immediately
            if main_content:
                for trash in main_content.find_all(["footer", "nav", "aside", "div.footer", "div.related-products"]):
                    trash.decompose()
            
            # 3. DESCRIPTION
            if main_content:
                desc_div = main_content.find("div", class_="product-description")
                if desc_div:
                    data["description"] = self.clean_text(desc_div.text)
                else:
                    # Fallback: Look for "Description" header and take the next sibling
                    header = main_content.find(lambda tag: tag.name in ["h2", "h3", "h4"] and "Description" in tag.text)
                    if header:
                        data["description"] = self.clean_text(header.find_next("p").text)
                    else:
                        ps = main_content.find_all("p")
                        if ps: data["description"] = self.clean_text(max(ps, key=lambda p: len(p.text)).text)
            
            if not data["description"] or "Test Type:" in data["description"]:
                data["description"] = "Description extraction failed."

            # 4. TEST TYPES (The Surgical Fix using your HTML Screenshot)
            found_types = set()
            
            # Strategy: Find the text "Test Type:"
            # Look for the specific structure: <p> ... Test Type: ... <span class="product-catalogue__key">
            
            # Find any element containing "Test Type:"
            label_node = soup.find(string=re.compile("Test Type:"))
            
            if label_node:
                # The node is usually a text node inside a <p>. Get the parent <p>.
                parent_p = label_node.find_parent()
                
                if parent_p:
                    # Now look for the keys ONLY inside this paragraph or its children
                    keys = parent_p.find_all("span", class_="product-catalogue__key")
                    for k in keys:
                        letter = k.get_text(strip=True)
                        if letter in self.type_map:
                            found_types.add(self.type_map[letter])

            # Fallback: Check Breadcrumbs if the "Test Type:" text wasn't found
            if not found_types:
                breadcrumbs = soup.find_all("nav", class_="breadcrumb")
                for bc in breadcrumbs:
                    for t in self.type_map.values():
                        if t in bc.get_text():
                            found_types.add(t)

            data["test_type"] = list(found_types) if found_types else ["Unknown"]

        except Exception as e:
            print(f"[WARN] Error parsing {url}: {e}")
        
        self.assessments.append(data)

    def save(self):
        with open(OUTPUT_FILE, "w", encoding='utf-8') as f:
            json.dump(self.assessments, f, indent=4, ensure_ascii=False)

if __name__ == "__main__":
    scraper = SHLScraper()
    scraper.crawl()