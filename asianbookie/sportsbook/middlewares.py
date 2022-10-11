# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware \
    as BaseRetryMiddleware


class TitanRetryMiddleware(BaseRetryMiddleware):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    def process_response(self, request, response, spider):
        if request.meta.get('dont_retry', False):
            return response

        # if response._encoding is None and response._headers_encoding() is not None \
        #         and response._body_declared_encoding() is not None \
        #         and response._headers_encoding() != response._body_declared_encoding():
        #     return response.replace(encoding=response._body_declared_encoding())

        # if len(response.body) < 100:
        #     if response.encoding == 'utf-8':
        #         request = request.replace(encoding='gb18030')
        #     if response.encoding == 'gb18030':
        #         request = request.replace(encoding='cp1252')
        #     return self._retry(request, "wrong_encoding", spider) or response

        if response.status in self.retry_http_codes:
            reason = super.response_status_message(response.status)
            return self._retry(request, reason, spider) or response
        return response


class SportsbookDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
