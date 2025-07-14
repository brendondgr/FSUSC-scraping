import scrapy
from scrapy.crawler import CrawlerProcess

class FsuscSpider(scrapy.Spider):
    name = "fsusc"

    def __init__(self, start_url, depth, *args, **kwargs):
        super(FsuscSpider, self).__init__(*args, **kwargs)
        self.start_urls = [start_url]
        self.max_depth = int(depth)
        # Using a dictionary to store sets of URLs for each depth
        self.urls_by_depth = {i: set() for i in range(1, self.max_depth + 1)}
        self.visited_urls = set()

    def start_requests(self):
        self.visited_urls.add(self.start_urls[0])
        yield scrapy.Request(self.start_urls[0], callback=self.parse, meta={'depth': 1})

    def parse(self, response):
        depth = response.meta.get('depth', 1)

        # If the request was redirected to another domain, ignore it.
        if not response.url.startswith("https://www.sc.fsu.edu") or "404-error" in response.url:
            return
        # Stop crawling if max depth is reached
        if depth > self.max_depth:
            return
        
        # Add the successfully crawled URL to our list for this depth
        final_url = response.url.split('#')[0]
        self.urls_by_depth[depth].add(final_url)

        # Discover new links on the page and create requests for the next depth level
        if depth < self.max_depth:
            for href in response.css('a::attr(href)').getall():
                # Resolve relative URLs
                url = response.urljoin(href)
                # Split URL at # if present
                base_url = url.split('#')[0]
                if (base_url not in self.visited_urls and 
                    base_url.startswith("https://www.sc.fsu.edu") and
                    not any(x in base_url for x in [
                        "/colloquium",
                        "/attachments/",
                        "/faculty-meetings/",
                        "/graduate/courses/",
                        "/undergraduate/courses/",
                        "/images/",
                        "/defenses/",
                        "/news-and-events/",
                        "/xpo",
                        "/links?",
                        "/tags/",
                        "/cilab",
                        "newsletter/",
                        "/archive/",
                        "/video",
                        
                        
                    ])):
                    self.visited_urls.add(base_url)
                    yield scrapy.Request(base_url, callback=self.parse, meta={'depth': depth + 1})

    def closed(self, reason):
        # When the spider finishes, write the collected URLs to a file
        with open("../urls.txt", "w") as f:
            for depth_level in range(1, self.max_depth + 1):
                urls = sorted(list(self.urls_by_depth[depth_level]))
                if urls:
                    # f.write(f"Depth {depth_level}\n")
                    for url in urls:
                        f.write(f"{url}\n")
                    f.write("\n")

def gather_urls(start_url, depth, replace_urls=False):
    import os
    if os.path.exists("../urls.txt"):
        if replace_urls:
            print("urls.txt found, deleting it.")
            os.remove("../urls.txt")
        else:
            print("urls.txt already exists. To overwrite, set replace-urls to True.")
            return

    # Settings for the crawler process
    process = CrawlerProcess(settings={
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
        'DOWNLOAD_DELAY': 0.25,  # Politeness delay
        'LOG_LEVEL': 'INFO',
    })

    # Start the crawl
    process.crawl(FsuscSpider, start_url=start_url, depth=depth)
    process.start()
