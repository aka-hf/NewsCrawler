# -*- coding: utf-8 -*-
import asyncio

from argon_log import logger
from base.base_spider import BaseSpider
from model.news import NewsCategory, Source
from news.sztv.request_handler import sztv_request_handler
from news.sztv.data_parser import SZTVNewsDataParser
from parse.news_parse import get_news_content
from save.database_handler import DatabaseHandler
import asyncio
from playwright.async_api import async_playwright

async def fetch_rendered_html(url: str, wait_time: int = 30000) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        await page.goto(url)
        await page.wait_for_timeout(wait_time)
        html = await page.content()
        await browser.close()
        return html


class SZTVNewsSpider(BaseSpider):
    def __init__(self):
        super().__init__()
        self.request_handler = sztv_request_handler
        self.data_parser = SZTVNewsDataParser()
        self.database_handler = DatabaseHandler()
        self.latest_china_news_url = ""
        # self.news_url = "https://www.sztv.com.cn/ysz/zx/tj/80463016.shtml"
        self.news_url = "https://www.sztv.com.cn/news/"
        # self.news_url = "https://apix.scms.sztv.com.cn/api/com/article/getArticleList"  # 根据实际新闻列表页调整

    async def fetch_latest_china_news(self):
        logger.warning("暂不支持该新闻类型的抓取")


    async def fetch_hot_news(self):
        """
        抓取深圳卫视新闻。
        """
        await self.fetch_and_process_news(
            url=self.news_url,
            category=NewsCategory.LATEST_CHINA.value,  # 根据实际分类调整
            source=Source.SZTV.value,
            log_prefix="深圳卫视新闻",
            parse_method=self.data_parser.parse_news_list,
        )

    async def fetch_and_process_news(
        self,
        url: str,
        category: str,
        source: str,
        log_prefix: str,
        parse_method: callable,
    ):
        # params = {
        # 'tenantId': 'ysz',
        # 'catalogId': '6552',
        # 'page': '1',
        # 'banner': '1',
        # "pageSize": '20'
        # }
        logger.info(f"开始抓取{log_prefix}...")
        response_text = await fetch_rendered_html(url)
        # logger.info(f"{response_text}")
        
        if response_text:
            json_data = parse_method(response_text)
            if json_data:
                tasks = [self.process_news(news) for news in json_data]
                news_content = await asyncio.gather(*tasks)
                news_content = [news for news in news_content if news]
                if self.to_database:
                    await self.database_handler.insert_or_update_news(
                        news_content,
                        category=category,
                        source=source,
                    )
                if self.storage_enabled:
                    try:
                        filepath = self.storage_handler.save(
                            news_content, source_name=source
                        )
                        logger.info(f"{log_prefix} 已保存到文件: {filepath}")
                    except Exception as e:
                        logger.error(f"{log_prefix} 保存新闻数据失败: {e}")
                logger.info(f"成功抓取 {len(news_content)} 条{log_prefix}。")
        logger.info(f"{log_prefix}抓取完成。")

    async def process_news(self, news):
        """
        处理单条新闻：获取 HTML 并解析新闻内容。
        """
        allowed_keys = ["title", "author", "publish_time", "content", "images", "url"]

        news_html = await fetch_rendered_html(news["url"])

        if news_html:
            news_content = get_news_content(news_html)
            news_content["url"] = news["url"]
            logger.debug(f"深圳卫视新闻:{news_content}")
            filtered_data = {k: news_content[k] for k in allowed_keys if k in news_content}

            return filtered_data
        else:
            logger.error(f"获取深圳卫视新闻 HTML 失败: {news['url']}")
            return None

if __name__ == "__main__":
    spider = SZTVNewsSpider()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(spider.fetch_hot_news())