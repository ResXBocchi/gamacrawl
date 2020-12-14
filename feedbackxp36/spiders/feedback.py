# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import FormRequest, Request
from feedbackxp36.items import Feedbackxp36Item


class FeedbackSpider(scrapy.Spider):
    name = 'feedback'
    allowed_domains = ['xp.gama.academy']
    start_urls = ['https://xp.gama.academy']

    def parse(self, response):
        authenticity_token = response.xpath('//*[@id="new_user_account"]/input[2]/@value').extract_first()
        user_account = input('Insira seu email: ')
        user_password = input('Insira sua senha: ')
        yield FormRequest('https://xp.gama.academy/entrar',
                            formdata={'authenticity_token' : authenticity_token,
                                      'user_account[email]': user_account,
                                      'user_account[password]':user_password},
                            callback=self.parse_after_login)

    def parse_after_login(self,response):

        feedbacks = response.urljoin(response.xpath('//*[@id="application-body"]/div[2]/a[4]/@href').extract_first())

        yield scrapy.Request(feedbacks, callback=self.parse_extract)

        

    def parse_extract(self,response):
        for i in range(1,100):
            item = Feedbackxp36Item()
            quebom= response.xpath('//*[@id="application-body"]/div[2]/div/div/blockquote[{}]/p[1]/text()'.format(i)).extract_first()
            quetal=response.xpath('//*[@id="application-body"]/div[2]/div/div/blockquote[{}]/p[2]/text()'.format(i)).extract_first()
            quepena=response.xpath('//*[@id="application-body"]/div[2]/div/div/blockquote[{}]/p[3]/text()'.format(i)).extract_first()

            if quebom != None or quetal != None or quepena != None:
                item['quebom'] = quebom
                item['quetal'] = quetal
                item['quepena'] = quepena

                yield item


