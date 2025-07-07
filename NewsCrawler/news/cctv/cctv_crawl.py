# -*- coding: utf-8 -*-
# Date:2025-01-24 09 59
import asyncio

from argon_log import logger
from base.base_spider import BaseSpider
from model.news import NewsCategory, Source
from news.cctv.data_parser import CCTVNewsDataParser
from news.cctv.request_handler import cctv_request_handler
from parse.news_parse import get_news_content
from save.database_handler import DatabaseHandler


class CCTVNewsSpider(BaseSpider):
    def __init__(self):
        super().__init__()  # 调用基类初始化
        self.request_handler = cctv_request_handler
        self.data_parser = CCTVNewsDataParser()
        self.database_handler = DatabaseHandler()  # 初始化数据库操作模块
        self.latest_china_news_url = (
            "https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/china_1.jsonp"
        )
        self.hot_news_url = "https://news.cctv.com/2019/07/gaiban/cmsdatainterface/page/news_1.jsonp?cb=news"

    async def fetch_hot_news(self):
        """
        抓取CCTV新闻-热门新闻。
        """
        # 如果热门新闻 URL 未设置，直接返回
        if not self.hot_news_url:
            logger.warning("热门新闻 URL 未设置，跳过抓取。")
            return

        await self.fetch_and_process_news(
            url=self.hot_news_url,
            category=NewsCategory.HOT.value,
            source=Source.CCTV.value,
            log_prefix="CCTV新闻-热门新闻",
            parse_method=self.data_parser.parse_hot_news_data,
        )

    async def fetch_latest_china_news(self):
        """
        抓取CCTV新闻-最新国内新闻。
        """
        await self.fetch_and_process_news(
            url=self.latest_china_news_url,
            category=NewsCategory.LATEST_CHINA.value,
            source=Source.CCTV.value,
            log_prefix="CCTV新闻-最新国内新闻",
            parse_method=self.data_parser.extract_json_from_china,
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
            if json_data:
                # 并发请求新闻页面的 HTML
                tasks = [self.process_news(news) for news in json_data]
                news_content = await asyncio.gather(*tasks)
                logger.debug(f"{news_content}")
                # 过滤掉空值（抓取失败的新闻）
                news_content = [news for news in news_content if news]
                if self.to_database:
                    # 批量插入或更新新闻数据到数据库
                    await self.database_handler.insert_or_update_news(
                        news_content,
                        category=category,
                        source=source,
                    )

                # 记录抓取的新闻数量
                logger.info(f"成功抓取 {len(news_content)} 条{log_prefix}。")
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
                if self.dingtalk_notifier.enabled:
                    await self.dingtalk_notifier.send_combined_news_notification(
                        news_content, title=f"{log_prefix}汇总"
                    )
        logger.info(f"{log_prefix}抓取完成。")

    async def process_news(self, news):
        """
        处理单条新闻：获取 HTML 并解析新闻内容。

        :param news: 单条新闻数据
        """
        allowed_keys = ["title", "author", "publish_time", "content", "images", "url"]
        
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
    spider = CCTVNewsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.fetch_latest_china_news())
