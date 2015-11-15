# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = "phone-list"
    allowed_domains = ["thephonedatabase.com"]

    start_urls = []

    for i in xrange(0,1082,10):
        start_urls.append('http://www.thephonedatabase.com/ajax_search.php?ajax=true&q=All_Phones&s=%s&e=%s&u=0' % (i, i))

    def parse(self, response):
        for sel in response.css('div .textlong a'):
            full_url = response.urljoin(sel.xpath('@href').extract()[0])
            title = sel.xpath('text()').extract()[0]
            yield scrapy.Request(full_url, callback=self.parse_question, meta = {'title': title})

    def parse_question(self, response):
        result = {'title': response.meta['title']}
        for sel in response.xpath('//div[@class="group"]'):
            features = sel.xpath('div[@class="feature"]/text()').extract()
            values = sel.xpath('div[@class="text"]/text()').extract()

            for feature, value in zip(features, values):
                result[feature] = value

        yield result