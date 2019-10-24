# !/usr/bin/python
# -*- coding:utf-8 -*-
# author : liaohuan

'''
1. 使用scrapy_splash处理ajax请求数据
2. 存储使用items和pipelines
'''
import json
import re

from scrapy_splash import SplashRequest
from scrapy import Spider, Selector, Request

from U17Spider.items import U17SpiderItem, U17ImagesItem


class U17Spider(Spider):
    name = 'u17'
    url = 'http://www.u17.com/comic_list/th99_gr99_ca99_ss99_ob0_ac0_as0_wm0_co99_ct99_p1.html?order=2'

    def start_requests(self):
        # 地址所对应的源码信息
        # 分析:若源码中可以获取想要的数据,则使用scrapy.Request即可
        #      若获取的数据需要经过ajax/js加载后才能获取,则需要使用scrapy_splash.SplashRequest

        lua_script = '''
        function main(splash, args)    
            splash:go(args.url)                 
            splash:wait(1)   
            next = splash:select(".next")
            next:mouse_click()
            splash:wait(1)
            return splash:html()
        end
        '''
        yield SplashRequest(url=self.url, callback=self.parse_list, args={"wait": 1})
        # for i in range(2,5):
        yield SplashRequest(url=self.url,callback=self.parse_list, args={'lua_source':lua_script,"wait":1}, endpoint='execute')


    # 爬取每一页的漫画列表
    def parse_list(self, response):
        # 回调方法,用于处理url地址所对应的相应内容
        # print(response.text)
        result = Selector(response)
        lis = result.xpath('//*[@id="all_comic_list"]/li')
        for li in lis:
            href = li.xpath('./a/@href').extract()[0]
            # print(href)
            yield Request(url=href, callback=self.detail_parse)


    # 获取漫画中的信息,包括:漫画名字,章节列表,章节url
    def detail_parse(self, response):
        result = Selector(response)
        item = U17SpiderItem()
        item['name'] = result.xpath('//*[@class="comic_info"]/div[1]/h1/text()').extract()[0].strip()
        # print(name)
        item['img'] = result.xpath('//*[@class="cover"]/a/img/@src').extract_first()
        # print(img)
        # //*[@id="chapter"]
        chapter_list = result.xpath('//*[@id="chapter"]/li')
        chapters = []
        i = 0
        for chapter in chapter_list:
            i += 1
            if i == 6:
                break
            data = {
                'title': chapter.xpath('./a/@title').extract()[0],
                'href': chapter.xpath('./a/@href').extract()[0]
            }

            # 获取章节详情图片的请求
            yield SplashRequest(url=data['href'], callback=self.parse_chapter)

            chapters.append(data)
        # print(chapters)

        item['chapters'] = chapters
        yield item


    # 获取章节的所有漫画url
    def parse_chapter(self, response):
        html = response.text

        try:
            patterns = re.compile('image_pages: ({.*?}),')
            pages = json.loads(patterns.findall(html)[0])
            for key in pages.keys():
                new_url = response.url + '#image_id=' + key
                print(new_url)
                yield SplashRequest(url=new_url, callback=self.parse_chapter_pages)
        except:
            result = Selector(response)
            item = U17ImagesItem()
            i = 0
            while 1:
                i += 1
                item['img_url'] = result.xpath(f'//*[@class="comic_read_img"]/div[{i}]/img/@src').extract_first()
                # TODO:图片路径为空
                if not item['img_url']:
                    break
                names = result.xpath('//*[@class="comic_name"]')
                # TODO:章节名字出错
                item['name'] = names.xpath('./text()').extract_first().split()[0]
                item['chapter_name'] = names.xpath('./span/text()').extract_first()
                item['page_num'] = str(i)

                yield item



    # 根据章节url,获取每一页漫画内容
    def parse_chapter_pages(self, response):
        result = Selector(response)
        item = U17ImagesItem()
        name = result.xpath('//*[@id="readtop"]/h1/a/text()').extract_first()
        page_num = result.xpath('//*[@id="readbottom"]/strong/em/text()').extract_first()
        one_img_name = result.xpath('//*[@id="current_chapter_name"]/text()').extract_first()
        one_img_url = result.xpath('//*[@id="current_read_image"]/img[2]/@src').extract_first()
        # print(one_img_url)
        item['name'] = name
        item['chapter_name'] = one_img_name
        item['page_num'] = page_num
        item['img_url'] = one_img_url
        yield item



