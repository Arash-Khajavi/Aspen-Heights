from langchain.tools import Tool
from datetime import datetime
from langchain_core.utils.pydantic import BaseModel
from langchain_openai.chat_models  import ChatOpenAI
from langchain.agents import create_tool_calling_agent
# Example of a Pydantic model for the tool
from langchain_core.tools import tool
from pydantic import BaseModel
from langchain_core.tools import tool
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup  # ✅ Correct
# Define the argument schema for the tool
from langchain.tools import Tool
from datetime import datetime
def save_to_txt(data: str, filename: str = "research_output.txt"):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data successfully saved to {filename}"
save_tool = Tool(
    name="save_text_to_file",
    func=save_to_txt,
    description="Saves structured research data to a text file.",
)


# print(data)
# if __name__ == "__main__":
#     tool = SearchMHG()
#     result = tool.invoke("fetch mhg.html data")
#     print(result)

    # Print a preview of the first 500 chars of each page for debugging
    # data = SearchMHG()
    # print(data)
    # for page_name, info in data.items():

    #     if "full_text" in info:
    #         print(info["full_text"])
import requests
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import json
import re
from langchain.tools import BaseTool
# def info_m():
#     #    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#        filehandle = open('mhg.html')
#     # formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

#     #    b=open(filename, "a", encoding="utf-8")
#     #    resp = requests.get(filename)
#     #    print(f"Requests status code: {resp.status_code}")
#     #    print(resp.text[:500])  # first 500 chars for debugging
#        n=str(filehandle).find("<body>")
#        n1=str(filehandle).find("</html>")
#        soup = BeautifulSoup(str(filehandle)[n:n1],'html.parser')
#        print(f"scraped successfully {soup}")
# print(info_m())
# class SearchMSG(BaseTool):
#     name: str='mhg.html'
#     description: str='Scrapes through the mhg.html file and extracts data'
#     def _run(self, query: str) -> str:
#         """Scrapes through the mhg.html file and extracts data"""
#         info_m()
#         return "Scrapes through the mhg.html file and extracts data"

#     # async def _arun(self, query: str) -> str:
#     #     raise NotImplementedError("Async not supported")
# sav= Tool(
#     name="extract extra info",
#     func=info_m(),
#     description=" Collects data from the mhg.html file",
# )
# print(SearchMSG)
# ---------------------------------------
# Scraper functions with debug prints
# ---------------------------------------

def fetch_with_requests(url: str):
    try:
        resp = requests.get(url)
        resp.raise_for_status()
        print(f"✅ Requests status code: {resp.status_code}")
        print(resp.text[:500])  # first 500 chars for debugging
        soup = BeautifulSoup(resp.text, "html.parser")
        if len(soup.get_text(strip=True)) > 200:
            print("Requests content seems OK")
            return soup
        else:
            print("⚠️ Requests content too short, fallback to JS")
            return None
    except Exception as e:
        print(f"❌ Requests failed: {e}")
        return None

def fetch_with_playwright(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # show browser
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(10000)  # wait 5 seconds for JS
        html = page.content()
        print("✅ Playwright fetched HTML (first 1000 chars):")
        print(html)
        browser.close()
        return BeautifulSoup(html, "html.parser")

def fetch_page(url: str):
    soup = fetch_with_requests(url)
    if not soup:
        soup = fetch_with_playwright(url)
    return soup

# ---------------------------------------
# Structured extraction
# ---------------------------------------

def extract_structured_info(soup):
    text = soup.get_text(separator="\n", strip=True)
    emails = re.findall(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    phones = re.findall(r"\+?\d[\d\s-]{7,}\d", text)
    steps = [h.get_text(strip=True) for h in soup.find_all("h2") if "STEP" in h.get_text(strip=True).upper()]
    return {
        "full_text": text,
        "emails": list(set(emails)),
        "phones": list(set(phones)),
        "steps": steps
    }

# ---------------------------------------
# Scrape multiple pages
# ---------------------------------------

def scrape_aquila():
    "search this website in order to fetch data regarding applying to AQUILA school based in dubai. you should also consider the scholarships"
    "and the types of scholarships they offer."
    base = "https://ahbs.ae"
    pages = {
        "Admissions": "/admissions/",
        "How to Apply": "/how-to-apply'",
        "Admissions Policy": "/admissions-policy/",
        "Contact Us": "/contact-us/",
        'Scholarships' :' /ahbs-scholarships/'
    }

    data = {}
    for name, path in pages.items():
        url = base + path
        print(f"\n--- Fetching {name} page ---")
        soup = fetch_page(url)
        if soup:
            info = {"title": soup.title.string if soup.title else None}
            info.update(extract_structured_info(soup))
            data[name] = info
        else:
            data[name] = {"error": "Failed to fetch"}

    # Save to JSON
    with open("aquila_data.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    print("📂 Data saved to aquila_data.json")
    return data

# ---------------------------------------
# LangChain Tool wrapper
# ---------------------------------------

class AquilaTool(BaseTool):
    name: str = "aquila_scraper"
    description: str = "Scrapes Aquila School pages and extracts structured info."

    def _run(self, query: str) -> str:
        """Scrapes Aquila School pages and saves the data to JSON."""
        scrape_aquila()
        return "Scraping completed. Data saved to aquila_data.json"

    async def _arun(self, query: str) -> str:
        raise NotImplementedError("Async not supported")

if __name__ == "__main__":
    tool = AquilaTool()
    result = tool.invoke("fetch aquila school data")
    print(result)

    # Print a preview of the first 500 chars of each page for debugging
    data = scrape_aquila()
    for page_name, info in data.items():
        print(f"\n=== {page_name} ===")
        if "full_text" in info:
            print(info["full_text"])
        else:
            print(info)


