import argparse
import os
from code.scrape import gather_urls
from code.extract import process_urls
from code.gemini import refine_all_raw_data

class Module:
    def __init__(self, starting_url, depth, replace_urls, get_raw_data, refine_data):
        self.starting_url = starting_url
        self.depth = depth
        self.replace_urls = replace_urls
        self.get_raw_data = get_raw_data
        self.refine_data = refine_data
        
        self.api_key = None
        if self.refine_data:
            self.check_api_key()
        
        self.group_dictionary = {
            "TechDocuments": {"names": ["/tech-docs"], "url": "https://www.sc.fsu.edu/computing/tech-docs/"},
            "Courses": {"names": ["/courses", "/index.php?"], "url": "https://www.sc.fsu.edu/courses"},
            "People": {"names": ["/people"], "url": "https://www.sc.fsu.edu/people"},
            "RoomReservations": {"names": ["/room-reservations"], "url": "https://www.sc.fsu.edu/room-reservations"},
            "Links": {"names": ["/links"], "url": "https://www.sc.fsu.edu/links"},
            "Graduate": {"names": ["graduate"], "url": "https://www.sc.fsu.edu/graduate"},
            "Undergraduate": {"names": ["undergraduate"], "url": "https://www.sc.fsu.edu/undergraduate"},
            "Computing": {"names": ["computing"], "url": "https://www.sc.fsu.edu/computing"},
            "Committees": {"names": ["committees"], "url": "https://www.sc.fsu.edu/committees"},
            "FAQ": {"names": ["faq"], "url": "https://www.sc.fsu.edu/faq"},
        }
        
        self.run()
    
    def run(self):
        self.check_parameters()
        if self.get_raw_data:
            print(f"Starting scrape for {self.starting_url} with depth {self.depth}")
            gather_urls(self.starting_url, self.depth, self.replace_urls)
            print("Scraping complete. Results are in urls.txt")

            print("Extracting text from URLs...")
            process_urls(self.group_dictionary)
            print("Text extraction complete. Results are in raw_data/")

        if self.refine_data:
            print("Refining data...")
            refine_all_raw_data(self.api_key)
            print("Data refinement complete. Results are in refined_data/")
        
    def check_api_key(self):
        if os.path.exists("api_key.txt"):
            with open("api_key.txt", "r") as f:
                self.api_key = f.read().strip()
        else:
            print("Google Gemini API key file ('api_key.txt') not found.")
            print("To get an API key, visit https://aistudio.google.com/app/apikey")
            api_key = input("Please enter your API key: ").strip()
            with open("api_key.txt", "w") as f:
                f.write(api_key)
            self.api_key = api_key
            print("API key saved to api_key.txt")

    def check_parameters(self):
        if not isinstance(self.depth, int) or self.depth < 1:
            raise ValueError("Depth must be an integer and at least 1")
        if not self.starting_url.startswith('http'):
            raise ValueError("Starting URL must be a valid URL (e.g., http://example.com)")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape a website to a certain depth.")
    parser.add_argument('--starting-url', type=str, default="https://www.sc.fsu.edu/",
                        help='The URL to start scraping from.')
    parser.add_argument('--depth', type=int, default=2,
                        help='How many links deep to scrape. Default is 2.')
    parser.add_argument('--replace-urls', action='store_true',
                        help='If set, deletes urls.txt if it exists. Otherwise, the script will not run if urls.txt exists.')
    parser.add_argument('--get-raw-data', action='store_true',
                        help='If set, gets information from URL to create the Raw Data.')
    parser.add_argument('--refine-data', action='store_true',
                        help='If set, refines the raw data using the Gemini API.')
    
    args = parser.parse_args()
    
    Module(args.starting_url, args.depth, args.replace_urls, args.get_raw_data, args.refine_data)