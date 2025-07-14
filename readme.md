# FSUSC Website Scraper

## Description

This project is designed to scrape the Florida State University Scientific Computing (FSUSC) department website. It uses a combination of Scrapy and BeautifulSoup to crawl the site and extract textual content from its pages. The primary goal is to gather and structure this information so it can be effectively used as a knowledge base for a Retrieval-Augmented Generation (RAG) model.

After the raw data is scraped, it is processed using the Google Gemini 2.5 Flash API to refine and clean the data, ensuring it is in a structured and easily interpretable format for the Language Model.

## Installation

These instructions use Conda for environment management.

1.  **Create a Conda environment:**
    ```bash
    conda create -n fsusc_scrape python=3.10
    ```

2.  **Activate the environment:**
    ```bash
    conda activate fsusc_scrape
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **API Key:**
    Create a file named `api_key.txt` in the root directory and place your Google Gemini API key inside it.

## Usage

The main script for running the scraper is `main.py`. You can modify its behavior using the following command-line parameters.

### Parameters

*   `--starting-url`: The URL where the scraper will begin.
    *   **Type:** `string`
    *   **Default:** `https://www.sc.fsu.edu/`
    *   **Example:** `python main.py --starting-url https://www.sc.fsu.edu/research`

*   `--depth`: Specifies the maximum depth to crawl from the starting URL. A depth of 1 will only scrape the initial page and the pages it links to.
    *   **Type:** `integer`
    *   **Default:** `2`
    *   **Example:** `python main.py --depth 3`

*   `--replace-urls`: If this flag is included, the existing `urls.txt` file will be deleted before the scrape begins. Otherwise, the script will not run if `urls.txt` is present.
    *   **Type:** `boolean` (flag)
    *   **Example:** `python main.py --replace-urls`

*   `--get-raw-data`: If this flag is included, the scraper will run and extract the raw text from the web pages.
    *   **Type:** `boolean` (flag)
    *   **Example:** `python main.py --get-raw-data`

*   `--refine-data`: If this flag is included, the script will process the files in `raw_data/` using the Gemini API and save the results to `refined_data/`.
    *   **Type:** `boolean` (flag)
    *   **Example:** `python main.py --refine-data`

### Running the Scraper

To run the scraper with default settings:
```bash
python main.py
```

To run with custom parameters:
```bash
python main.py --starting-url <YOUR_URL> --depth <YOUR_DEPTH> --replace-urls
```

## Project Structure

```
.
├── main.py               # Main script to run the scraper and extractor
├── code/
│   ├── scrape.py             # Contains the web scraping logic (Scrapy/BeautifulSoup)
│   ├── extract.py            # Extracts and cleans text from scraped URLs
│   └── gemini.py             # Refines the raw data using the Gemini API
├── raw_data/             # Stores the raw text extracted from web pages
├── readme.md             # This file
├── refined_data/         # Stores the cleaned and structured data from Gemini
├── requirements.txt      # Python dependencies
└── urls.txt              # A list of URLs to be scraped
```
