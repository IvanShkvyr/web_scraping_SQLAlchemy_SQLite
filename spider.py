from datetime import datetime, date
from multiprocessing import Process

import scrapy
from scrapy.crawler import CrawlerProcess
from itemadapter import ItemAdapter

from conect_to_db import session
from models import Author, Quote, Tag, TagToQuote


class AuthorSpider(scrapy.Spider):
    name = 'authors'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):
            yield response.follow(url=self.start_urls[0] + quote.xpath('span/a/@href').get(),
             callback=self.parse_author)

        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)

    def parse_author(self, response):
        content = response.xpath("/html//div[@class='author-details']")
        fullname = content.xpath("h3/text()").get().strip()
        date_of_birth = content.xpath("p/span[@class='author-born-date']/text()").get().strip()  # April 28, 1926
        date_of_birth = datetime.strptime(date_of_birth, '%B %d, %Y').date()
        lint_to_info = response.url


        # заготовка на базу даних
        record = Author(fullname=fullname, date_of_birth=date_of_birth, lint_to_info=lint_to_info)
        session.add(record)
        session.commit()




class QuotesSpider(scrapy.Spider):
    name = 'quotes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        for quote in response.xpath("/html//div[@class='quote']"):

            tags = quote.xpath("div[@class='tags']/a/text()").extract()
            author_fullname = quote.xpath("span/small/text()").get()
            author = session.query(Author).filter(Author.fullname == author_fullname).first().__dict__['id']
            quote = quote.xpath("span[@class='text']/text()").get()[1:-1]

           # запис в базу цитат
            record_quote = Quote(text=quote, author_id=author)
            session.add(record_quote)
            session.commit()


# запис в базу тегів
            for tag in tags:
                if not session.query(Tag).filter(Tag.text == tag).first():

                    record_tag = Tag(text=tag)
                    session.add(record_tag)
                    session.commit()

                    tag_id = session.query(Tag).filter(Tag.text == tag).first().__dict__['id']
                    quote_id = session.query(Quote).filter(Quote.text == quote).first().__dict__['id']

    # запис в базу звязків
                    record_tag_to_quote = TagToQuote(tag_id=tag_id, quote_id=quote_id)
                    session.add(record_tag_to_quote)
                    session.commit()


        next_link = response.xpath("//li[@class='next']/a/@href").get()
        if next_link:
            yield scrapy.Request(url=self.start_urls[0] + next_link)



def main(spider):
    process = CrawlerProcess()
    process.crawl(spider)
    process.start()

if __name__ == '__main__':

    pro1 = Process(target=main, args=(AuthorSpider, ))
    pro2 = Process(target=main, args=(QuotesSpider, ))
    pro1.start()
    pro1.join()

    pro2.start()
    pro2.join()
