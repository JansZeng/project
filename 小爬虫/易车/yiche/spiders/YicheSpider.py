# coding:utf-8
import scrapy
from .util import fixjson, json2csv_chexing, json2csv_chexing3
import logging
import json, re


class YicheSpider(scrapy.Spider):
    name = "yiche"
    domain = "http://car.bitauto.com"
    start_urls = ['http://car.bitauto.com']  # 起始url
    f_store = 'data_cars.csv'
    f = open(f_store, 'w')

    def parse(self, response):
        print('--------程序开始------------')
        # 获取车辆品牌列表
        car_ids = response.xpath('//div[@class="item-brand"]/@data-id').extract()
        car_names = response.xpath('//div[@class="item-brand"]/@data-name').extract()
        car_list = [i for i in zip(car_ids, car_names)]

        for car in car_list:
            print(car)
            id = car[0]
            url = f'http://car.bitauto.com/xuanchegongju/?mid={id}'
            # 关闭URL 去重 dont_filter=True
            request = scrapy.Request(url=url, callback=self.get_car_page_url, dont_filter=True)
            # 通过 request 传递参数
            request.meta['mb'] = car[1]
            yield request

    def get_car_page_url(self, response):
        """获取品牌所有页面url"""
        # print('获取品牌所有页面url')
        xpath = '//*[@id="pagination-list"]/div/div/a/@href'
        urls = map(lambda x: self.domain + x, response.xpath(xpath).extract())
        for url in urls:
            # 关闭URL 去重 dont_filter=True
            request = scrapy.Request(url=url, callback=self.parse_chexing2, dont_filter=True)
            # 通过 request 传递参数
            request.meta['mb'] = response.meta['mb']
            print(request)
            yield request

    def parse_chexing2(self, response):
        """获取车型配置数据"""
        xpath = '//div[@class="search-result-list-item"]/a/@href'
        urls = map(lambda x: self.domain + x + 'peizhi/', response.xpath(xpath).extract())

        for url in urls:
            # 关闭URL 去重 dont_filter=True
            request = scrapy.Request(url=url, callback=self.parse_chexing3, dont_filter=True)
            # 通过 request 传递参数
            request.meta['mb'] = response.meta['mb']
            yield request

    def parse_chexing3(self, response):
        """保存数据"""
        data = response.xpath('//script/text()').extract()
        # 车型参数 列表
        carCompareJson = re.findall(r'var carCompareJson = (.*?);', data[7])
        if carCompareJson:
            # response传递的过来的车辆品牌名称
            mb = response.meta['mb']
            car_result = json2csv_chexing3(carCompareJson[0], mb)
            self.f.write(car_result)
            self.log('Save car %s' % car_result.split(',')[6])
            yield
        # print(result)
        # 选装包
        # optionalPackageJson = re.findall(r'var optionalPackageJson = (.*?)$', data[7], re.S)
        #
        # if optionalPackageJson:
        #     optional_result = optionalPackageJson[0].strip()
        #     if len(optional_result) > 2:
        #         print('****************')
        #         print(optional_result)
        #         print(type(optional_result), type(eval(optional_result)))
        #     else:
        #         print('mymymymymy')
        # if optionalPackageJson:
        #

