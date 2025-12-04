import os
import time
import json
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://indiankanoon.org/search/"
# DOCUMENTS_FILE = "legal_documents.json"

queries = ["agriculture land", "residential land", "land dispute"]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
}

def fetch_case_links(query, max_pages=10):
    """Fetch normalized case links (/doc/) for a given query."""
    links = []
    for page in range(1, max_pages + 1):
        url = f"{BASE_URL}?formInput={query.replace(' ', '+')}&pagenum={page}"
        res = requests.get(url, headers=HEADERS)
        if res.status_code != 200:
            break

        soup = BeautifulSoup(res.text, "html.parser")
        case_links = soup.select("div.result_title")
        links.append(f"{case_links}")
        if not case_links:
            break

        # for a in case_links:
        #     href = soup.select_one('div.result_title a').get('href')
        #     # print(href)
        #     if not href:
        #         continue

        #     if "/docfragment/" in href:
        #         # /docfragment/<id>/ → /doc/<id>/
        #         doc_id = href.split("/")[2]
        #         full_link = f"https://indiankanoon.org/doc/{doc_id}/"
        #     elif href.startswith("/doc/"):
        #         full_link = "https://indiankanoon.org" + href
        #     else:
        #         continue

        #     # print(full_link)
        #     links.append(full_link)

        time.sleep(3)  # be polite
    return links

def fetch_case_text(url):
    """Fetch case judgment text from a case page."""
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        return None

    soup = BeautifulSoup(res.text, "html.parser")
    # judgment = soup.find("div", {"class": "judgements"})
    # judgment = soup.find("div", {"class": "akoma-ntoso"})
    title = fetch_case_title(soup) or "No title"
    judgment = soup.find("div", {"class": "judgments"}) \
            or soup.find("div", {"class": "akoma-ntoso"}) \
            or soup.find("div", {"id": "content"})
    text = judgment.get_text(separator="\n", strip=True) if judgment else None

    return title, text

def fetch_case_title(soup):
    """Extract case title from a case page soup."""
    title_tag = soup.find("h1", {"class": "doc_title"}) \
                or soup.find("h2", {"class": "doc_title"})\
                or soup.find("h1")
    if title_tag:
        return title_tag.get_text(strip=True)
    return None

def main():
    document = {}

    for query in queries:
        print(f"Searching for: {query}")
        links = fetch_case_links(query, max_pages=10)
        print(f"Found {len(links)} cases for '{query}'")
        # print(links)
        with open(f"../data/document_links_{query}.txt", "w", encoding="utf-8") as f:
            for link in links:
                f.write(link)

        # for i, link in enumerate(links, 1):
        #     # title, text = fetch_case_text(link)
        #     title, text = None, None if fetch_case_text(link) is None else fetch_case_text(link)
        #     if text:
        #         document = {
        #             "query": query,
        #             "url": link,
        #             "title": title,
        #             "content": text
        #         }
        #             # Save to JSON
        #         with open(f"legal_documents/{query}_doc_{i}.json", "w", encoding="utf-8") as f:
        #             json.dump(document, f, ensure_ascii=False, indent=2)
        #         print(f"Fetched {i}/{len(links)} for '{query}'")
        #     time.sleep(2)

    # Save to JSON
    # with open(DOCUMENTS_FILE, "w", encoding="utf-8") as f:
    #     json.dump(documents, f, ensure_ascii=False, indent=2)

    # print(f"\nSaved {len(documents)} documents into {DOCUMENTS_FILE}")

if __name__ == "__main__":
    main()

'''from bs4 import BeautifulSoup
import re

# read file
link_files = ["../data/document_links_agriculture_land.txt", "../data/document_links_land_dispute.txt", "../data/document_links_residential_land.txt"]
hrefs = []
links = []
for file in link_files:
    with open(file, "r", encoding="utf-8") as f:
        content = f.read()

    # parse
    soup = BeautifulSoup(content, "html.parser")

    # extract hrefs
    hrefs = [a["href"] for a in soup.find_all("a", href=True)]

    for href in hrefs:
        match = re.match(r"^/docfragment/(\d+)", href)
        if match:
            links.append(f"doc/{match.group(1)}")


# save to file
with open("../data/document_links.txt", "w", encoding="utf-8") as f:
    for link in links:
        f.write(link + "\n")
'''