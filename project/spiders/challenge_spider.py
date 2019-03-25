import scrapy


class ChallengeSpider(scrapy.Spider):
    name = "challenge"
    first = True
    count = 0
    result = {}
    
    def start_requests(self):
        url = 'https://www.drukzo.nl.joao.hlop.nl/python.php'
        yield scrapy.Request(url=url, callback=self.parse)

    
        
    def parse(self, response):
        OPTION_SELECTOR = 'option::text'
        
        if self.first == False:
            last_option = response.meta['item']
            print("last option = ", last_option, self.count)
        else:
            last_option = None
            self.first = False
        
        drops = response.xpath('//select[contains(@id, "drop")]')
        #print("Drop =", drops, self.count)
        if len(drops) <= self.count:
                yield {'Decision Tree': self.result}
        else:        
            options = drops[self.count].css(OPTION_SELECTOR).getall()
            print("options = ", options)
        
            self.count = self.count + 1
        
            for option in options:
                request = scrapy.FormRequest.from_response(
                    response,
                    formdata={'type': 'submit', 'value' :'submit'},
                    callback=self.parse)
                request.meta['item'] = option
                yield request

                if last_option is not None:
                    self.result[last_option] = options
                
