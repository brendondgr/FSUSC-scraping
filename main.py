import argparse
from scrape import gather_urls
from extract import process_urls

class Module:
    def __init__(self, starting_url, depth, replace_urls):
        self.starting_url = starting_url
        self.depth = depth
        self.replace_urls = replace_urls
        
        self.api_key = open("api_key.txt", "r").read()
        
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
        print(f"Starting scrape for {self.starting_url} with depth {self.depth}")
        gather_urls(self.starting_url, self.depth, self.replace_urls)
        print("Scraping complete. Results are in urls.txt")

        print("Extracting text from URLs...")
        process_urls(self.group_dictionary)
        print("Text extraction complete. Results are in raw_data/")
        
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
    
    args = parser.parse_args()
    
    Module(args.starting_url, args.depth, args.replace_urls)