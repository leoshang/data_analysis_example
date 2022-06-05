# -*- coding: utf-8 -*-

# Scrapy settings for sportsbook project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#     http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
#     http://scrapy.readthedocs.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'livescore'

SPIDER_MODULES = ['sportsbook.spiders']
NEWSPIDER_MODULE = 'sportsbook.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
# USER_AGENT = 'sportsbook (+http://www.yourdomain.com)'

# Configure maximum concurrent requests performed by Scrapy (default: 16)
USER_AGENT = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:44.0) Gecko/20100101 Firefox/44.0"

# Obey robots.txt rules
# ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
CONCURRENT_REQUESTS = 1
CONCURRENT_ITEMS = 1
CONCURRENT_REQUESTS_PER_DOMAIN = 1

DEFAULT_REQUEST_HEADERS = {
   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
   'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
}

# https://stackoverflow.com/questions/8768439/how-to-give-delay-between-each-requests-in-scrapy
# default 0.25  # 250 ms of delay
# DOWNLOAD_DELAY = 10

# If you set 1 for both start and max delay, it will wait 1 second in each request.
# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_START_DELAY = 3
# AUTOTHROTTLE_MAX_DELAY = 10

SPIDER_MIDDLEWARES = {
    'scrapy.spidermiddlewares.referer.RefererMiddleware': True
    # 'sportsbook.middlewares.SportsbookDownloaderMiddleware': 888
}

FILES_STORE = "/Users/leishang/helenstreet/python/sportsbook/output/odds_history/csv/"
IMAGES_STORE = "/Users/leishang/helenstreet/python/sportsbook/output/image_download/"

ITEM_PIPELINES = {
    'sportsbook.pipelines.Win007XslxExportPipeline': 800
}

# for export into csv not for xslx. XSLX export is directly done in Win007XslxExportPipeline
FEED_EXPORTERS = {
    'csv': 'sportsbook.exporter.oddsexporter.OddsExporter'
}

# for export into csv.
FIELDS_TO_EXPORT = [
    'match_id',
    'match_time',
    'bookie_id',
    'bookie_name_en',
    'bookie_name_cn',
    'open_home_win',
    'open_draw',
    'open_guest_win'
    'end_home_win',
    'end_draw',
    'end_guest_win',
    'open_home_prob',
    'open_draw_prob',
    'open_guest_prob',
    'end_home_win_prob',
    'end_draw_prob',
    'end_guest_win_prob'
]

# Configure a delay for requests for the same website (default: 0)
# See http://scrapy.readthedocs.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
# DOWNLOAD_DELAY=3
# The download delay setting will honor only one of:
# CONCURRENT_REQUESTS_PER_DOMAIN=16
# CONCURRENT_REQUESTS_PER_IP=16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Enable or disable downloader middlewares
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'sportsbook.middlewares.MyCustomDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See http://scrapy.readthedocs.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.telnet.TelnetConsole': None,
# }

# Enable and configure the AutoThrottle extension (disabled by default)
# See http://doc.scrapy.org/en/latest/topics/autothrottle.html
# NOTE: AutoThrottle will honour the standard settings for concurrency and delay
# AUTOTHROTTLE_ENABLED=True
# The initial download delay
# AUTOTHROTTLE_START_DELAY=5
# The maximum download delay to be set in case of high latencies
# AUTOTHROTTLE_MAX_DELAY=60
# Enable showing throttling stats for every response received:
# AUTOTHROTTLE_DEBUG=False

# Enable and configure HTTP caching (disabled by default)
# See http://scrapy.readthedocs.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
# HTTPCACHE_ENABLED=True
# HTTPCACHE_EXPIRATION_SECS=0
# HTTPCACHE_DIR='httpcache'
# HTTPCACHE_IGNORE_HTTP_CODES=[]
# HTTPCACHE_STORAGE='scrapy.extensions.httpcache.FilesystemCacheStorage'
