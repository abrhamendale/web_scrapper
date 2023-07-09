import scrapy
class ArticleSpider(scrapy.Spider):
    name='article'
    def start_requests(self):
        urls = [
                'https://en.wikipedia.org/wiki/Ball',
                'https://www.ebay.de/sch/i.html?_from=R40&_trksid=p2047675.m570.l1313&_nkw=galaxy+23&_sacat=0',
                #'%28programming_language%29',
                'https://en.wikipedia.org/wiki/Functional_programming',
                'https://en.wikipedia.org/wiki/Monty_Python']
        return [scrapy.Request(url=url, callback=self.parse)
                for url in urls]
    def parse(self, response):
        url = response.url
        title = response.css('span.s-item__price').getall()
        print('URL is: {}'.format(url))
        print('Title is: {}'.format(title))
