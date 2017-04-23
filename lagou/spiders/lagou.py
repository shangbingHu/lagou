import scrapy


class QuotesSpider(scrapy.Spider):
    name = "lagou"

    def start_requests(self):
        urls = [
            'https://www.lagou.com',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse1(self, response):
        filename = 'rsp.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(type(response.css('a')))
        logfile = 'log'
        divs = response.css('div.mainNavs')
        with open(logfile, 'wb') as f:
            for div in divs:
                for title in div.css('a::text'):
                    #yield(title.extract().encode('utf-8') + "\n")
                    yield({"title": title.extract().encode('utf-8')})
        self.log('Saved file %s' % filename)



    def parse(self, response):
        filename = 'rsp.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        logfile = 'log'
        divs = response.xpath('//div[@class="mainNavs"]')
        with open(logfile, 'wb') as f:
            for div in divs:
                for title in div.xpath('//a/text()'):
                    #yield(title.extract().encode('utf-8') + "\n")
                    yield({"title": title.extract().encode('utf-8')})
        self.log('Saved file %s' % filename)

