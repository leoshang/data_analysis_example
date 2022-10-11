from scrapy import cmdline
cmdline.execute("scrapy crawl sportsbookspider -s FEED_EXPORT_ENCODING=utf-8".split())
