# -*- coding: utf-8 -*-
import scrapy

from yjbys.items import YjbysItem


class YjbysSpider(scrapy.Spider):
    name = 'yjbys'
    allowed_domains = ['yjbys.com']
    host = "http://www.yjbys.com"
    start_urls = [host + "/xuanjianghui/"]

    def parse(self, response):
        div_list = response.xpath("//div[@class='xjhschool']")
        for div in div_list:
            item = YjbysItem()
            item['company'] = div.xpath("./div[3]/a/text()").extract_first()
            # 学校有两种格式 满足一种即可
            school = div.xpath("./div[4]/span/a/text()").extract_first()
            if school is None:
                school = div.xpath("./div[4]/span/text()").extract_first()
            item['school'] = school
            # 两种格式满足其一
            holding_time = div.xpath("./div[1]/font/text()").extract_first()
            if holding_time is None:
                holding_time = div.xpath("./div[1]/text()").extract_first()
            sj = div.xpath("./div[2]/text()").extract_first()
            item['holding_time'] = holding_time+" "+str(sj)
            item['addr'] = div.xpath("./div[4]/font/text()").extract_first()
            item['href'] = self.host + div.xpath("./div[3]/a/@href").extract_first()
            yield item
        #翻页 暂无
        # response.xpath("")
