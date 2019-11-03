# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class SteamGameItem(scrapy.Item):
    # 基本信息
    name = scrapy.Field()
    developer = scrapy.Field()
    publisher = scrapy.Field()
    releaseDate = scrapy.Field()
    gameType = scrapy.Field()
    tags = scrapy.Field()
    # 评价
    recentReview = scrapy.Field()
    recentGoodReviewRate = scrapy.Field()
    totalReview = scrapy.Field()
    totalGoodReviewRate = scrapy.Field()
    # 价格
    originalPrice = scrapy.Field()
    finalPrice = scrapy.Field()
    # 特性
    singlePlay = scrapy.Field()
    multiPlay = scrapy.Field()
    coop = scrapy.Field()
    onlineCoop = scrapy.Field()
    onlineMultiPlay = scrapy.Field()
    crossPlatform = scrapy.Field()
    steamAchievement = scrapy.Field()
    steamTradeCard = scrapy.Field()
    steamWorkshop = scrapy.Field()
    steamCloud = scrapy.Field()
    steamRank = scrapy.Field()
    stat = scrapy.Field()
    levelEditor = scrapy.Field()
    IAP = scrapy.Field()
    controllerSupport = scrapy.Field()
    VRSupport = scrapy.Field()
    earlyAccess = scrapy.Field()
    # 配置信息
    minimumCPU = scrapy.Field()
    minimumMemory = scrapy.Field()
    minimumHardDrive = scrapy.Field()
    minimumVideoCard = scrapy.Field()
    recommendCPU = scrapy.Field()
    recommendMemory = scrapy.Field()
    recommendHardDrive = scrapy.Field()
    recommendVideoCard = scrapy.Field()
    # 简体中文支持
    simpleChineseUI = scrapy.Field()
    simpleChineseAudio = scrapy.Field()
    simpleChineseSubtitle = scrapy.Field()

class SaleRankItem(scrapy.Item):
    # 基本信息
    itemKey = scrapy.Field()
    name = scrapy.Field()
    releaseDate = scrapy.Field()
    # 支持平台
    supportWin = scrapy.Field()
    supportMac = scrapy.Field()
    supportLinux = scrapy.Field()
    # 价格信息
    originalPrice = scrapy.Field()
    nowPrice = scrapy.Field()
    discount = scrapy.Field()
    # 评价信息
    reviewCount = scrapy.Field()
    goodReviewRate = scrapy.Field()