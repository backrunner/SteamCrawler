# -*- coding: utf-8 -*-
import scrapy
from steamcrawler.items import SteamGameItem

class StoreSpider(scrapy.Spider):
    name = 'store'
    allowed_domains = ['store.steampowered.com']
    # 种子URL
    #start_urls = ['https://store.steampowered.com/search/?category1=998']

    def start_requests(self):
        for page in range(1,1433):
            yield scrapy.Request('https://store.steampowered.com/search/?category1=998&page='+str(page), self.parse)

    def parse(self, response):
        for url in response.xpath('//*[@id="search_resultsRows"]/a/@href').getall():
            yield scrapy.Request(url, callback=self.parse_per_game)
        # 获取下一页的链接
        #next_page = response.xpath('//*[@class="search_pagination_right"]/a[last()]/@href').get()
        #if next_page:
        #    yield scrapy.Request(next_page, callback=self.parse)
        #else:
        #    print('There is no more page, crawling completed.')

    def parse_per_game(self, response):
        item = SteamGameItem()
        # 基本信息
        item["name"] = response.xpath('//*[@class="apphub_AppName"]/text()').get()
        item["developer"] = ','.join(response.xpath('//*[@id="developers_list"]/a/text()').getall())
        publishers = response.xpath('//*[@class="summary column"]/a/text()').getall()
        if len(publishers) > 0:
            item['publisher'] = publishers[-1]
        item["releaseDate"] = response.xpath('//*[@class="date"]/text()').get()
        item["tags"] = ','.join(response.xpath('//*[@class="glance_tags popular_tags"]/a/text()').re(r'\S+'))
        # 评价
        reviewData = response.xpath('//*[@class="nonresponsive_hidden responsive_reviewdesc"]/text()').re('(?![0-9]+\sdays)(?![0-9]+\s天)[0-9,%]+')
        if len(reviewData) == 2:
            # 只有全部没有最近
            item["totalReview"] = reviewData[0]
            item["totalGoodReviewRate"] = reviewData[1]
        elif len(reviewData) == 4:
            item["recentReview"] = reviewData[0]
            item["recentGoodReviewRate"] = reviewData[1]
            item["totalReview"] = reviewData[2]
            item["totalGoodReviewRate"] = reviewData[3]
        # 价格
        normalPrices = response.xpath('//*[@class="game_area_purchase_game"]/div[@class="game_purchase_action"]/div[@class="game_purchase_action_bg"]/div[@class="game_purchase_price price"]/text()').re('[0-9,]+')
        if len(normalPrices) < 1:
            # 是打折中的游戏
            discountOriginalPrice = response.xpath('//*[@class="game_area_purchase_game"]/div[@class="game_purchase_action"]/div[@class="game_purchase_action_bg"]/div[@class="discount_block game_purchase_discount"]/div[@class="discount_prices"]/div[@class="discount_original_price"]/text()').re('[0-9,]+')
            discountFinalPrice = response.xpath('//*[@class="game_area_purchase_game"]/div[@class="game_purchase_action"]/div[@class="game_purchase_action_bg"]/div[@class="discount_block game_purchase_discount"]/div[@class="discount_prices"]/div[@class="discount_final_price"]/text()').re('[0-9,]+')
            if len(discountOriginalPrice) > 0 and len(discountFinalPrice) > 0:
                item["originalPrice"] = discountOriginalPrice[0]
                item["finalPrice"] = discountFinalPrice[0]
            else:
                item["originalPrice"] = 0
                item["finalPrice"] = 0
        else:
            item["originalPrice"] = normalPrices[0]
            item["finalPrice"] = normalPrices[0]
        # 特性
        specs = response.xpath('//*[@class="game_area_details_specs"]/a/text()').getall()
        for spec in specs:
            if spec == '单人':
                item['singlePlay'] = True
            elif spec == '多人':
                item['multiPlay'] = True
            elif spec == '在线多人':
                item['onlineMultiPlay'] = True
            elif spec == '合作':
                item['coop'] = True
            elif spec == '在线合作':
                item['onlineCoop'] = True
            elif spec == '跨平台联机游戏':
                item['crossPlatform'] = True
            elif spec == 'Steam 成就':
                item['steamAchievement'] = True
            elif spec == 'Steam 集换式卡牌':
                item['steamTradeCard'] = True
            elif spec == 'Steam 创意工坊':
                item['steamWorkshop'] = True
            elif spec == 'Steam 云':
                item['steamCloud'] = True
            elif spec == 'Steam 排行榜':
                item['steamRank'] = True
            elif spec == '统计':
                item['stat'] = True
            elif spec == '包含关卡编辑器':
                item['levelEditor'] = True
            elif spec == '应用内购买':
                item['IAP'] = True
            elif spec == '部分支持控制器':
                item['controllerSupport'] = 'Partial'
            elif spec == '完全支持控制器':
                item['controllerSupport'] = 'Completed'
        vrsupport = response.xpath('//*[@class="block_title vrsupport"]').getall()
        if len(vrsupport) > 0:
            item['VRSupport'] = True
        earlyaccess = response.xpath('//*[@class="early_access_header"]').getall()
        if len(earlyaccess) > 0:
            item['earlyAccess'] = True
        # 配置信息
        minimumLabels = response.xpath('//*[@data-os="win"]/div[1]/ul/ul/li/strong/text()')
        minumumProps = response.xpath('//*[@data-os="win"]/div[1]/ul/ul/li/text()').re('(?!需要 64 位处理器和操作系统)(^.*)')
        if len(minimumLabels) > 0 and len(minumumProps) > 0:
            minimumLabels = minimumLabels.getall()
            for i in range(len(minimumLabels)):
                if '处理器' in minimumLabels[i]:
                    item['minimumCPU'] = minumumProps[i]
                elif '内存' in minimumLabels[i]:
                    item['minimumMemory'] = minumumProps[i]
                elif '显卡' in minimumLabels[i]:
                    item['minimumVideoCard'] = minumumProps[i]
                elif '存储空间' in minimumLabels[i]:
                    item['minimumHardDrive'] = minumumProps[i]
        elif len(minimumLabels) > 0 and len(minumumProps) < 1:
            for i in range(len(minimumLabels)):
                if '处理器' in minimumLabels[i]:
                    if ':' in minimumLabels[i]:
                        t = minimumLabels[i].split(':')
                        if len(t) == 2:
                            item['minimumCPU'] = t[1]
                    elif '：' in minimumLabels[i]:
                        t = minimumLabels[i].split('：')
                        if len(t) == 2:
                            item['minimumCPU'] = t[1]
                elif '内存' in minimumLabels[i]:
                    if ':' in minimumLabels[i]:
                        t = minimumLabels[i].split(':')
                        if len(t) == 2:
                            item['minimumMemory'] = t[1]
                    elif '：' in minimumLabels[i]:
                        t = minimumLabels[i].split('：')
                        if len(t) == 2:
                            item['minimumMemory'] = t[1]
                elif '显卡' in minimumLabels[i]:
                    if ':' in minimumLabels[i]:
                        t = minimumLabels[i].split(':')
                        if len(t) == 2:
                            item['minimumVideoCard'] = t[1]
                    elif '：' in minimumLabels[i]:
                        t = minimumLabels[i].split('：')
                        if len(t) == 2:
                            item['minimumVideoCard'] = t[1]
                elif '存储空间' in minimumLabels[i]:
                    if ':' in minimumLabels[i]:
                        t = minimumLabels[i].split(':')
                        if len(t) == 2:
                            item['minimumHardDrive'] = t[1]
                    elif '：' in minimumLabels[i]:
                        t = minimumLabels[i].split('：')
                        if len(t) == 2:
                            item['minimumHardDrive'] = t[1]
        recommendLabels = response.xpath('//*[@data-os="win"]/div[@class="game_area_sys_req_rightCol"]/ul/ul/li/strong/text()')
        recommendProps = response.xpath('//*[@data-os="win"]/div[@class="game_area_sys_req_rightCol"]/ul/ul/li/text()').re('(?!需要 64 位处理器和操作系统)(^.*)')
        if len(recommendLabels) > 0 and len(recommendProps) > 0:
            recommendLabels = recommendLabels.getall()
            for i in range(len(recommendLabels)):
                if '处理器' in recommendLabels[i]:
                    item['recommendCPU'] = recommendProps[i]
                elif '内存' in recommendLabels[i]:
                    item['recommendMemory'] = recommendProps[i]
                elif '显卡' in recommendLabels[i]:
                    item['recommendVideoCard'] = recommendProps[i]
                elif '存储空间' in recommendLabels[i]:
                    item['recommendHardDrive'] = recommendProps[i]
        elif len(recommendLabels) > 0 and len(recommendProps) < 1:
            for i in range(len(recommendLabels)):
                if '处理器' in recommendLabels[i]:
                    if ':' in recommendLabels[i]:
                        t = recommendLabels[i].split(':')
                        if len(t) == 2:
                            item['recommendCPU'] = t[1]
                    elif '：' in recommendLabels[i]:
                        t = recommendLabels[i].split('：')
                        if len(t) == 2:
                            item['recommendCPU'] = t[1]
                elif '内存' in recommendLabels[i]:
                    if ':' in recommendLabels[i]:
                        t = recommendLabels[i].split(':')
                        if len(t) == 2:
                            item['recommendMemory'] = t[1]
                    elif '：' in recommendLabels[i]:
                        t = recommendLabels[i].split('：')
                        if len(t) == 2:
                            item['recommendMemory'] = t[1]
                elif '显卡' in recommendLabels[i]:
                    if ':' in recommendLabels[i]:
                        t = recommendLabels[i].split(':')
                        if len(t) == 2:
                            item['recommendVideoCard'] = t[1]
                    elif '：' in recommendLabels[i]:
                        t = recommendLabels[i].split('：')
                        if len(t) == 2:
                            item['recommendVideoCard'] = t[1]
                elif '存储空间' in recommendLabels[i]:
                    if ':' in recommendLabels[i]:
                        t = recommendLabels[i].split(':')
                        if len(t) == 2:
                            item['recommendHardDrive'] = t[1]
                    elif '：' in recommendLabels[i]:
                        t = recommendLabels[i].split('：')
                        if len(t) == 2:
                            item['recommendHardDrive'] = t[1]
        # 简体中文支持
        unsupported = response.xpath('//*[@class="game_language_options"]/tr[@class="unsupported"]/td/text()')
        if len(unsupported) > 0:
            unsupportedLang = unsupported[0].re('\S+')
            if unsupportedLang == '简体中文':
                item['simpleChineseUI'] = False
                item['simpleChineseAudio'] = False
                item['simpleChineseSubtitle'] = False
                item['simpleChineseCompletedSupport'] = False
        else:
            simpleChineseSupport = response.xpath('//*[@class="game_language_options"]/tr[2]/td[@class="checkcol"]').getall()
            if len(simpleChineseSupport) > 0:
                if '✔' in simpleChineseSupport[0]:
                    item['simpleChineseUI'] = True
                if '✔' in simpleChineseSupport[1]:
                    item['simpleChineseAudio'] = True
                if '✔' in simpleChineseSupport[2]:
                    item['simpleChineseSubtitle'] = True
        yield item