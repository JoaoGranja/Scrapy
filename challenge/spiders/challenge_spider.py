import scrapy


class ChallengeSpider(scrapy.Spider):
    name = "challenge"
    start = True
    result = {}
    
    def start_requests(self):
        url = 'https://www.drukzo.nl.joao.hlop.nl/python.php'
        yield scrapy.Request(url=url, callback=self.parse)
        
    def parse(self, response):
        OPTION_SELECTOR = 'option::text'
        tree = {}

        # Get the last selected option and last drop number
        if self.start == False:
            last_option = response.meta['item']
            last_drops  = response.meta['drop_nr']
            print("Drop number = ", last_drops)
        else:
            self.start = False
            last_drops = 0
            last_option = None

        # Get the drops
        drops = response.xpath('//select[contains(@id, "drop")]')
        if len(drops) == last_drops:
            # No more drops, so yield
            yield {'Decision Tree': self.result}
        else:
            # Get all options from last drop and iterate over them
            
            options = drops[len(drops)-1].css(OPTION_SELECTOR).getall()
            if last_option is not None:
                tree[last_option] = options
                print("Tree =", tree)
                self.result[last_option] = options
                
            for option in options:
                print("selected option = ", option)
                request = scrapy.FormRequest.from_response(
                    response,
                    formdata={'type': 'submit', 'value' :'submit', 'selected': option},
                    callback=self.parse)
                request.meta['item'] = option
                request.meta['drop_nr'] = len(drops)
                yield request 



