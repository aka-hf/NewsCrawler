# -*- coding: utf-8 -*-
# Date:2025-04-14 14 07
import asyncio

from argon_log import logger

from base.base_spider import BaseSpider
from model.news import NewsCategory, Source
from news.thepaper.data_parser import ThePaperNewsDataParser
from news.thepaper.request_handler import the_paper_request_handler
from parse.news_parse import get_news_content



class ThePaperNewsSpider(BaseSpider):
    def __init__(self):
        super().__init__()  # 调用基类初始化
        self.request_handler = the_paper_request_handler
        self.data_parser = ThePaperNewsDataParser()
        self.latest_china_news_url = ""
        self.hot_news_url = "https://cache.thepaper.cn/contentapi/wwwIndex/rightSidebar"

    async def fetch_latest_china_news(self):
        """
        抓取澎湃新闻-最新国内新闻。
        """
        logger.warning("暂不支持该新闻类型的抓取")

    async def fetch_hot_news(self):
        """
        抓取澎湃新闻-热门新闻。
        """
        await self.fetch_and_process_news(
            url=self.hot_news_url,
            category=NewsCategory.HOT.value,
            source=Source.THE_PAPER.value,
            log_prefix="澎湃新闻-热门新闻",
            parse_method=self.data_parser.parse_hot_news_data,
        )

    async def fetch_and_process_news(
        self,
        url: str,
        category: str,
        source: str,
        log_prefix: str,
        parse_method: callable,
    ):
        """
        抓取并处理新闻数据。

        :param url: 新闻数据的 URL
        :param category: 新闻分类
        :param source: 新闻来源
        :param log_prefix: 日志前缀
        :param parse_method: 解析数据的方法
        """
        logger.info(f"开始抓取{log_prefix}...")
        response = await self.request_handler.fetch_data_get(url)
        response_text = response.text
        if response_text:
            # 解析数据
            json_data = parse_method(response_text)
            # logger.info(f"{news_content}")
            if json_data:
                # 并发请求新闻页面的 HTML
                tasks = [self.process_news(news) for news in json_data]
                news_content = await asyncio.gather(*tasks)
                logger.debug(f"{news_content}")
                # 过滤掉空值（抓取失败的新闻）
                news_content = [news for news in news_content if news]
                # 保存新闻内容
                if self.storage_enabled:
                    try:
                        filepath = self.storage_handler.save(
                            news_content, source_name=source
                        )
                        logger.info(f"{log_prefix} 已保存到文件: {filepath}")
                    except Exception as e:
                        logger.error(f"{log_prefix} 保存新闻数据失败: {e}")
                # 发送整合后的新闻通知
                if self.feishu_talk_notifier.enabled:
                    await self.feishu_talk_notifier.send_multi_news_card(news_content)
                logger.info(f"成功抓取 {len(news_content)} 条{log_prefix}。")
        logger.info(f"{log_prefix}抓取完成。")

    async def process_news(self, news):
        """
        处理单条新闻：获取 HTML 并解析新闻内容。

        :param news: 单条新闻数据
        """
        allowed_keys = ["title", "publish_time", "content", "images", "url"]

        # 获取新闻页面的 HTML
        response = await self.request_handler.fetch_data_get(news["url"])
        news_html = response.text
        if news_html:
            news_content = get_news_content(news_html)
            news_content["url"] = news["url"]
            logger.debug(f"CCTV新闻:{news_content}")
            filtered_data = {k: news_content[k] for k in allowed_keys if k in news_content}

            return filtered_data
        else:
            logger.error(f"获取新闻 HTML 失败: {news['url']}")
            return None  # 返回空值表示抓取失败


if __name__ == "__main__":
    spider = ThePaperNewsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.fetch_hot_news())
