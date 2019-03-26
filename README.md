# Scrapy
The scope of this project is to present the basics of scraping a web page to collect specific data.

# Extracted data
This project extract options data from a dropdowns. The extracted data looks like this sample:

{'Decision Tree': {'A': ['C', 'B'], 'B': ['D', 'E'], 'C': ['D', 'E'], 'E': ['H', 'I', 'J'], 'D': ['H', 'I', 'J'], 'I': ['R'], 'J': ['R'], 'H': ['R']}}

# Running the spider

You can run a spider using the scrapy crawl command, such as:
$ scrapy crawl challenge

If you want to save the scraped data to a file, you can pass the -o option:
$ scrapy crawl challenge -o decisionTree.json
