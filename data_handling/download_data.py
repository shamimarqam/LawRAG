import os
import time
import json
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


BASE_URL = "https://indiankanoon.org/"
DOCUMENTS_FILE = "../data/legal_documents.json"
# https://indiankanoon.org/doc/1287305/

link_file = "../data/document_links.txt"


HEADERS = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/126.0 Safari/537.36"
}
titles = []

def fetch_case_text(url):
    """Fetch case judgment text from a case page."""
    res = requests.get(url, headers=HEADERS)
    if res.status_code != 200:
        return None

    soup = BeautifulSoup(res.text, "html.parser")
    # judgment = soup.find("div", {"class": "judgements"})
    # judgment = soup.find("div", {"class": "akoma-ntoso"})
    title = fetch_case_title(soup)
    titles.append(title)
    judgment = soup.find("div", {"class": "judgments"}) \
            or soup.find("div", {"class": "akoma-ntoso"}) \
            or soup.find("div", {"id": "content"})
    text = judgment.get_text(separator="\n", strip=True) if judgment else None

    return text


def fetch_links(link_file):
    links = []
    with open(link_file, "r", encoding="utf-8") as f:
        urls_list = [line.strip() for line in f if line.strip()]
    for l in urls_list:
        links.append(f"{BASE_URL}{l}")
    return links


def fetch_case_title(soup):
    """Extract case title from a case page soup."""
    title_tag = soup.find("h1", {"class": "doc_title"}) \
                or soup.find("h2", {"class": "doc_title"})\
                or soup.find("h1")
    if title_tag: 
        return title_tag.get_text(strip=True)
    else:
        return "No title"
    

def main():
    # documents = []
    links = fetch_links(link_file)
    i = 0
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # optional: run in background
    driver = webdriver.Chrome(options=options)
    for link in links:
        driver.get(link)
        # click the download button
        download_button = driver.find_element(By.ID, "pdfdoc")
        if download_button:
            download_button.click()
            print(f"Doc{i}")
        time.sleep(10)
        i=i+1  # adjust based on file size / download speed

    driver.quit()

        # text = fetch_case_text(link)
        # if text:
        #     title = titles[i]
        #     print(title)
        #     document = {
        #         "url": link,
        #         "content": text
        #     }
        #     documents.append(document)
        #     # with open(f"../legal_documents/{title}.json", "w", encoding="utf-8") as f:
        #     #     json.dump(document, f, ensure_ascii=False, indent=2)
        #     print(f"doc{i} added")
        #     i=i+1
        # time.sleep(2)

    # with open(DOCUMENTS_FILE, "w", encoding="utf-8") as f:
    #     json.dump(documents, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
