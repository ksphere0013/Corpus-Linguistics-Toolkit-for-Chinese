import requests
import json
import re
from bs4 import BeautifulSoup
from pathlib import Path
from opencc import OpenCC
from selenium import webdriver

# ============================================================
# 1. collect article URLs from archive pages
# ============================================================

# HTTP header to mimic a browser
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/151.0.0.0 Safari/537.36"
    )
}

# URL archive page for URL collection
archive_url = ("https://chinadigitaltimes.net/chinese/post-archives")

# fetch article URLs from the first 5 archive pages
driver = webdriver.Chrome()
article_links = []

for page in range(1, 6): # change the range to fetch different number of pages

    if page == 1:
        page_url = archive_url
    else:
        page_url = f"{archive_url}?dps_paged={page}" # alter the URL for subsequent pages; using f to allow variable interpolation in the string

    print(f"Fetching archive page: {page_url}")

    # use Selenium to load the page in a real browser, avoiding 403 errors
    driver.get(page_url)

    # parse the page with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")

    # iterate through all anchor tags and extract article URLs
    for link in soup.find_all("a", href=True):
        article_url = link["href"]

        if ("/chinese/" in article_url and article_url.endswith(".html")):
            if article_url not in article_links:
                article_links.append(article_url)

driver.quit()

print(f"Found {len(article_links)} article URLs") 


# ============================================================
# 2. collect articles and save as JSON
# ============================================================

# create output directory
output_dir = Path("data/raw")
output_dir.mkdir(parents=True, exist_ok=True)

# counter for article numbering and total characters amount
article_no = 1
total_characters = 0

# tool for Traditional to Simplified Chinese conversion
converter = OpenCC("t2s") 

# flag to skip "相关阅读(related readings)" section
skip_related = False 

# iterate through each article URL; extract and save data
for url in article_links:

    # fetch webpage
    response = requests.get(
        url,
        headers=headers
    )

    response.raise_for_status()

    # parse HTML content
    soup = BeautifulSoup(response.text, "html.parser")

    # --------------------------------------------------
    # 2.1 extract metadata
    # --------------------------------------------------

    # extract article title
    title_element = soup.find("h1")

    if title_element is None:
        print(f"Title not found: {url}")
        continue

    title = title_element.get_text(strip=True)

    # extract page text for metadata extraction
    page_text = soup.get_text(" ", strip=True) 

    # extract metadata field from the current line
    def extract_metadata_field(soup, label):
        label_element = soup.find(
            "strong",
            string=re.compile(re.escape(label)) 
        )

        if label_element is None:
            return None

        value_parts = []

        for element in label_element.next_siblings:
            if getattr(element, "name", None) == "br":
                break

            if hasattr(element, "get_text"):
                value_parts.append(
                    element.get_text(strip=True)
                )
            elif isinstance(element, str):
                value_parts.append(element.strip())

        value = "".join(value_parts).strip()

        return value if value else None

    # extract author
    author = extract_metadata_field(soup, "作者：")

    # skip articles without author information
    if not author:
        print(f"Skipped (no author information): {title}")
        continue

    # extract source
    source = extract_metadata_field(soup, "来源：")
    if not source:
        source = "China Digital Times"

    # extract topic
    topic = extract_metadata_field(soup, "主题归类：")
    if not topic:
        topic = "Unknown"

    # extract publication date
    publication_date = "Unknown"
    date_value = extract_metadata_field(soup, "发表日期：")
    if date_value:
        date_match = re.search(
            r"(\d{4})[.\-年]\s*(\d{1,2})[.\-月]\s*(\d{1,2})",
            date_value
        )
        if date_match:
            year, month, day = date_match.groups()
            publication_date = (
                f"{year}-{int(month):02d}-{int(day):02d}"
            )

    # identify copyright and license
    if author == "中国数字时代":
        copyright_holder = "China Digital Times"
        license = "CC BY-NC-SA 3.0"
    else:
        copyright_holder = author
        license = "Not specified"

    # --------------------------------------------------
    # 2.2 extract main article content
    # --------------------------------------------------

    # find the main article content
    article = soup.find("article")
    if article is None:
        print(f"Article content not found: {url}")
        continue


    # collect article text
    text = ""
    content_elements = article.find_all(["h2", "h3", "p"])

    for element in content_elements:

        content_text = element.get_text(strip=True)

        # stop before page metadata
        if content_text.startswith("所在分类："):
            break
        if content_text.startswith("标签："):
            break

        # detect "相关阅读(related readings)" section and skip it
        if content_text == "相关阅读：":
            skip_related = True
            continue

        # skip linked article titles under "相关阅读(related readings)" section
        if skip_related:
            if element.find("a"):
                continue
            skip_related = False

        # remove publication date
        if re.fullmatch(r"\d{4}年\d{1,2}月\d{1,2}日", content_text):
            continue

        # convert Traditional Chinese to Simplified Chinese
        content_text = converter.convert(content_text)
        if content_text:
           text += content_text + "\n"


    # create metadata dictionary
    metadata = {
        "title": title,
        "source": source,
        "url": url,
        "author": author,
        "published": publication_date,
        "genre": "Online News Article",
        "topic": topic,
        "copyright": copyright_holder,
        "license": license
    }

    # create corpus document dictionary
    document = {
        "id": f"cdt_{article_no:04d}",
        "text": text,
        "metadata": metadata
    }

    # save document as JSON
    output_file = (output_dir / f"cdt_{article_no:04d}.json")

    with output_file.open("w", encoding="utf-8") as f:

        json.dump(
            document, 
            f,
            ensure_ascii=False, # preserve Chinese characters in UTF-8
            indent=2 # print JSON with indentation for readability
        )

    # update counters
    article_no += 1
    total_characters += len(text)

    # print information
    print(f"Saved: {title}")
    print(f"Author: {author}")
    print(f"Source: {source}")    
    print(f"Published: {publication_date}")
    print(f"Topic: {topic}")
    print(f"Copyright: {copyright_holder}")
    print(f"License: {license}")
    print(f"Characters: {len(text)}")
    print(f"Total characters: {total_characters}")
    print(f"File: {output_file}")
    print("-" * 50)