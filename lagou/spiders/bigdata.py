import scrapy
import time
import json
#from lagou.items import BigDataItem


class QuotesSpider(scrapy.Spider):
    name = "bigdata"

    cookies = {"user_trace_token": "20170322232858-31ce943602014936a4a4551aa27e2f8a",
               "LGUID": "20170322232858-4506b76c-0f14-11e7-954f-5254005c3644",
               "index_location_city": "%E6%88%90%E9%83%BD",
               "JSESSIONID": "D70C324118F7A5EA8B3E648CD602D5C8",
               "SEARCH_ID": "dab5fb7fe734410e81919d63f0a79596",
               "_ga": "GA1.2.607030856.1492734795",
               "Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1492734795",
               "Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6": "1492734798",
               "LGRID": "20170421083318-1d77fbef-262a-11e7-8601-525400f775ce"}


    def start_requests(self):

        urls = [
            'https://www.lagou.com/jobs/positionAjax.json?pn={$PAGE}&kd=%E5%A4%A7%E6%95%B0%E6%8D%AE&city=%E6%88%90%E9%83%BD&needAddtionalResult=false'.replace("{$PAGE}", str(x)) for x in range(1, 8)
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse, cookies=self.cookies)

    def parse_job(self, response):
        positionId = response.meta['positionId']
        position_desc = '\n'.join(response.xpath('//dd[@class="job_bt"]/div/p/text()').extract())
        position_addr = response.xpath('//input[@name="positionAddress"]/@value').extract_first()
        return {'positionId': positionId, 'position_desc': position_desc, 'position_addr': position_addr}






        #filename = 'rsp.html'
        #with open(filename, 'wb+') as f:
        #    f.write(response.body)
        #self.log(type(response.css('a')))
        #logfile = 'log'
        #divs = response.css('div.mainNavs')
        #with open(logfile, 'wb') as f:
        #    for div in divs:
        #        for title in div.css('a::text'):
        #            #yield(title.extract().encode('utf-8') + "\n")
        #            yield({"title": title.extract().encode('utf-8')})
        #self.log('Saved file %s' % filename)



    def parse(self, response):
        result = json.loads(response.body)["content"]["positionResult"]["result"]
        filename = 'rsp.log'
        with open(filename, 'wb+') as f:
            f.write(str(result))

        for item in result:
            yield item
            url = "https://www.lagou.com/jobs/%s.html" % item['positionId']
            yield scrapy.Request(url=url, callback=self.parse_job, cookies=self.cookies, meta={"positionId": item['positionId']})

            #f.write(info[""])
        #logfile = 'log'
        #divs = response.xpath('//div[@class="mainNavs"]')
        #with open(logfile, 'wb') as f:
        #    for div in divs:
        #        for title in div.xpath('//a/text()'):
        #            #yield(title.extract().encode('utf-8') + "\n")
        #            yield({"title": title.extract().encode('utf-8')})
        #self.log('Saved file %s' % filename)

