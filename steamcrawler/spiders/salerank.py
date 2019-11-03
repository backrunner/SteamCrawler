import scrapy
from steamcrawler.items import SaleRankItem

class SaleRankSpider(scrapy.Spider):
    name = 'salerank'
    allowed_domains = ['store.steampowered.com']

    def start_requests(self):
        for page in range(1,10):
            yield scrapy.Request('https://store.steampowered.com/search/?filter=topsellers&page='+str(page), self.parse)

    def parse(self, response):
        item = SaleRankItem()
        page_res = response.xpath('//*[@id="search_resultsRows"]/a')
        for r in page_res:
            # 基本信息
            item['itemKey'] = r.xpath('./@data-ds-itemkey').get()
            item['name'] = r.xpath('./div[@class="responsive_search_name_combined"]/div/span[@class="title"]/text()').get()
            item['releaseDate'] = r.xpath('./div[@class="responsive_search_name_combined"]/div[@class="col search_released responsive_secondrow"]/text()').get()
            # 平台支持
            winSupport = r.xpath('./div[@class="responsive_search_name_combined"]/div/p/span[@class="platform_img win"]').getall()
            if (len(winSupport) > 0):
                item['supportWin'] = True
            macSupport = r.xpath('./div[@class="responsive_search_name_combined"]/div/p/span[@class="platform_img mac"]').getall()
            if (len(winSupport) > 0):
                item['supportMac'] = True
            linuxSupport = r.xpath('./div[@class="responsive_search_name_combined"]/div/p/span[@class="platform_img linux"]').getall()
            if (len(linuxSupport) > 0):
                item['supportLinux'] = True
            # 价格信息
            discount = r.xpath('./div[@class="responsive_search_name_combined"]/div[@class="col search_price_discount_combined responsive_secondrow"]/div[@class="col search_discount responsive_secondrow"]/span')
            if (len(discount) > 0):
                item['discount'] = discount[0].xpath('./text()').get()
            nowPrice = r.xpath('./div[@class="responsive_search_name_combined"]/div[@class="col search_price_discount_combined responsive_secondrow"]/div[@class="col search_price  responsive_secondrow"]/text()')
            if len(nowPrice) > 0:
                item['nowPrice'] = nowPrice.re('[0-9]+')[0]
                item['originalPrice'] = nowPrice.re('[0-9]+')[0]
            else:
                item['nowPrice'] = r.xpath('./div[@class="responsive_search_name_combined"]/div[@class="col search_price_discount_combined responsive_secondrow"]/div[@class="col search_price discounted responsive_secondrow"]/text()').re('[0-9]+')[0]
                item['originalPrice'] = r.xpath('./div[@class="responsive_search_name_combined"]/div[@class="col search_price_discount_combined responsive_secondrow"]/div[@class="col search_price discounted responsive_secondrow"]/span/strike/text()').re('[0-9]+')[0]
            # 评价信息
            tooltipHtml = r.xpath('div[@class="responsive_search_name_combined"]/div[@class="col search_reviewscore responsive_secondrow"]/span/@data-tooltip-html')
            if len(tooltipHtml) > 0:
                item['goodReviewRate'] = tooltipHtml.re('[0-9+%]')[0]
                item['reviewCount'] = tooltipHtml.re('[0-9,]+\s')[0]
                item['reviewCount'] = item['reviewCount'].replace(" ","")

            yield item