import re
from datetime import datetime
import scrapy
from scrapy.selector import Selector
import json
import time

class SCMPSpider(scrapy.Spider):
    name = "scmp_spider"
    start_urls = ['https://www.scmp.com/topics/us-china-relations']

    def parse(self, response):
        category_regex = r"[a-zA-Z-]*$"
        category = re.findall(category_regex, response.url)[0]

        content = response.xpath('//div[@sponsorimage]')

        for article in content:
            url = article.xpath('.//a[@class="article__link"]/@href').get()

            time = article.xpath('.//span[@class="author__status-left-time"]//text()').get()

            yield response.follow(url=url, callback=self.parse_article, dont_filter=False,
                                  meta={'url': url, 'category': category
                                      , 'time': time})

    def make_blurp(self, text: str, limit=420):
        if len(text) > limit:
            text = text[:limit]
        return text

    def parse_article(self, response):
        title = response.xpath('//meta[@name="cse_socialheadline"]//@content').get()
        url = SCMPSpider.base_url + response.request.meta['url']
        blurp = response.xpath('//meta[@name="cse_summary"]//@content').get()

        category = response.request.meta['category']
        article_date = response.request.meta['time']

        try:
            article_date = datetime.strptime(article_date, "%d %b %Y - %I:%M%p")  # converting into datetime object
        except ValueError:
            article_date = datetime.today()
        article_date = datetime.strftime(article_date, "%Y-%m-%d")  # converting into YYYY-MM-DD string

        # Dynamically loaded content
        content = response.xpath('//script[contains(.,"articleBody")]').get()

        pattern = r"(?is)<script[^>]*>(.*?)</script>"
        content = re.findall(pattern, content)[0]

        content = json.loads(content)
        text = content.get("articleBody")

        imgurl = content.get("image").get("url")
        tags = response.xpath('//meta[@property="article:tag"]//@content').getall()

        if not blurp or len(blurp) < 40:
            blurp = self.make_blurp(text)

        yield {
            'title': title,
            'imgurl': imgurl,
            'date': article_date,
            'blurp': blurp,
            'url': url,
            'text': text,
            'category': category,
            'source': self.name,
            'tags': tags
        }

