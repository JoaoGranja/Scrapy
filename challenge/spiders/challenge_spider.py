import scrapy


class ChallengeSpider(scrapy.Spider):
    name  = "challenge"
    last_drop = False
    first_option = ''
    count = 1
    decision_tree = {}
    
    def start_requests(self):
        url = 'https://www.drukzo.nl.joao.hlop.nl/python.php'
        yield scrapy.Request(url=url, callback=self.parse_first)

    def parse_first(self, response):
        OPTION_SELECTOR = 'option::text'
        tree = {}

        # Get all drops information
        drops = response.xpath('//select[contains(@id, "drop")]')
        self.count -= 1
        
        # Get all options from last drop and iterate over them
        options = drops[len(drops)-1].css(OPTION_SELECTOR).getall()
        print("drops....",len(drops))

        self.count += len(options)
        for i, selected_option in enumerate(options):
            #print("selected option = ", selected_option)
            self.first_option = selected_option
            tree[selected_option] = {}
            self.decision_tree = tree
            request = scrapy.FormRequest.from_response(
                response,
                formdata={'type': 'submit', 'value' :'submit', 'selected': selected_option},
                callback=self.parse)
            request.meta['item'] = selected_option
            request.meta['tree'] = self.decision_tree
            request.meta['total_drops'] = len(drops)
            yield request
            
    def parse(self, response):
        OPTION_SELECTOR = 'option::text'
        DROP_SELECTOR   = 'text'
        
        # Get the meta data
        tree                = response.meta['tree']
        previous_option     = response.meta['item']
        total_drops         = response.meta['total_drops']
        #print("Drop number = ", total_drops)
        #print("previous_option", previous_option)
        #print("Count", self.count)
        #print("Tree before", tree)
        #print("Decision Tree before", self.decision_tree)

        # Get all drops information
        drops = response.xpath('//select[contains(@id, "drop")]')
        self.count -= 1
            
        # Get all options from last drop and iterate over them
        options       = drops[len(drops)-1].css(OPTION_SELECTOR).getall()
        drop_list     = response.css('select::attr(id)').getall()
        selected_drop = drop_list[len(drop_list)-1]
        #print(drops[len(drops)-1])
        #print(options)
        #print(selected_drop)

        #Verify if last drop and last option was reached
        if total_drops == len(drops) and self.count == 0:
            yield {'Decision Tree': {self.first_option: self.decision_tree[self.first_option]}}

        if total_drops < len(drops):
            self.count += len(options)
            for i, selected_option in enumerate(options):
                print("selected option = ", selected_option)
                tree[previous_option][selected_option] = {}
                print("tree:", tree)
                if i == len(options)-1:
                    #self.decision_tree[previous_option].update(tree)
                    try:
                        self.decision_tree.update(tree)
                    except:
                        pass
                    print("result:", self.decision_tree)
                
                request = scrapy.FormRequest.from_response(
                    response,
                    formdata={'type': 'submit', 'value' :'submit', str(selected_drop):selected_option},
                    callback=self.parse)
                request.meta['item'] = selected_option
                request.meta['tree'] = tree[previous_option]
                request.meta['total_drops'] = len(drops)
                yield request
   


                    



