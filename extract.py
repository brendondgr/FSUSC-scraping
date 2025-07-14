import os
import requests
from bs4 import BeautifulSoup, Tag
from urllib.parse import urlparse

def get_filename_from_url(url, base_url="https://www.sc.fsu.edu"):
    """Generates a filename from a URL."""
    path = url.replace(base_url, "").strip('/')
    if not path:
        return "Home.txt"

    parts = path.split('/')
    if parts and '?' in parts[-1]:
        parts[-1] = parts[-1].split('?')[0]

    filename_parts = [p[0].upper() + p[1:] for p in parts if p]
    filename = "".join(filename_parts)
    return filename + ".txt"

def fetch_and_parse(url):
    """
    Fetches a URL and returns its title and text content, focusing on the main content area
    and excluding specific sections like 'prefooter' and sidebars.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        title = soup.title.string.strip() if soup.title and soup.title.string else "No Title Found"

        main_content = soup.find('main')
        if not main_content:
            main_content = soup.find(attrs={'role': 'main'})

        if not isinstance(main_content, Tag):
            print(f"Warning: No valid <main> or role='main' content found for {url}")
            return title, None
        
        # Remove the prefooter div by its ID
        prefooter = main_content.find('div', id='prefooter')
        if isinstance(prefooter, Tag):
            prefooter.decompose()

        # Remove elements with specified class names
        selectors_to_remove = [
            '.hidden-xs.hidden-sm.col-md-3',
            '.moduletable'
        ]
        for selector in selectors_to_remove:
            for unwanted_element in main_content.select(selector):
                unwanted_element.decompose()
            
        text = main_content.get_text(separator='\n', strip=True)
        return title, text
    except requests.exceptions.RequestException as e:
        print(f"Could not fetch {url}: {e}")
    except Exception as e:
        print(f"Error processing {url}: {e}")
    return None, None

def process_urls(group_dictionary):
    """
    Processes URLs from urls.txt, groups them, and extracts text into files.
    """
    if not os.path.exists("raw_data"):
        os.makedirs("raw_data")

    try:
        with open("urls.txt", "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        print("urls.txt not found. Please run the scraper first.")
        return

    url_groups = {group: [] for group in group_dictionary}
    ungrouped_urls = []

    for url in urls:
        found_group = False
        for group, details in group_dictionary.items():
            for name_part in details["names"]:
                if name_part in url:
                    url_groups[group].append(url)
                    found_group = True
                    break
            if found_group:
                break
        if not found_group:
            ungrouped_urls.append(url)

    # Process grouped URLs
    for group, urls_in_group in url_groups.items():
        if not urls_in_group:
            continue
        
        file_path = os.path.join("raw_data", f"{group}.txt")
        with open(file_path, "w", encoding="utf-8") as f:
            for i, url in enumerate(urls_in_group):
                title, text = fetch_and_parse(url)
                if title and text:
                    f.write(f"Title: {title}\n")
                    f.write(f"url: {url}\n\n")
                    f.write(text)
                    if i < len(urls_in_group) - 1:
                        f.write("\n\n---\n\n")
    
    # Process ungrouped URLs
    for url in ungrouped_urls:
        filename = get_filename_from_url(url)
        file_path = os.path.join("raw_data", filename)
        
        title, text = fetch_and_parse(url)
        if title and text:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(f"Title: {title}\n")
                f.write(f"url: {url}\n\n")
                f.write(text) 