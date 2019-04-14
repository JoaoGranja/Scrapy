import scrapy


class ChallengeSpider(scrapy.Spider):
    name = "challenge"
    start = True
    decision_tree = {}
    
    def start_requests(self):
        url = 'https://www.drukzo.nl.joao.hlop.nl/python.php'
        yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        OPTION_SELECTOR = 'option::text'
        
        # Get the last selected option and total drops number
        if self.start == False:
            tree         = response.meta['tree']
            last_option  = response.meta['item']
            total_drops  = response.meta['total_drops']
            #print("Drop number = ", total_drops)
        else:
            self.start = False
            total_drops = 0
            tree = {}
            last_option = None

        # Get all drops information
        drops = response.xpath('//select[contains(@id, "drop")]')
        #print("DROPS :", len(drops))
        #print(drops)
        
        if len(drops) == total_drops:
            # No more drops, so no more request is needed
            yield {'Decision Tree': self.decision_tree}
        else:
            # Get all options from last drop and iterate over them
            options = drops[len(drops)-1].css(OPTION_SELECTOR).getall()
            print(options)
                
            for i, selected_option in enumerate(options):
                print("selected option = ", selected_option)
                tree[selected_option] = {}
                if last_option is not None and i == len(options)-1:
                    print("before result:", self.decision_tree)
                    self.decision_tree[last_option] = tree
                    print("last_option = ", last_option)       
                    print("tree:", tree)
                    print("result:", self.decision_tree)
                    
                request = scrapy.FormRequest.from_response(
                    response,
                    formdata={'type': 'submit', 'value' :'submit', 'selected': selected_option},
                    callback=self.parse)
                request.meta['item'] = selected_option
                request.meta['tree'] = tree[selected_option]
                request.meta['total_drops'] = len(drops)
                yield request 



