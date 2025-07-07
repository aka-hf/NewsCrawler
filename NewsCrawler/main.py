import argparse
import asyncio
from typing import Callable, Awaitable
from datetime import datetime
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from news.baidu.baidu_crawl import BaiduNewsSpider
from news.cctv.cctv_crawl import CCTVNewsSpider
from news.netease.netease_crawl import NeteaseNewsSpider
from news.sina.sina_crawl import SinaNewsSpider
from news.tencent.tencent_crawl import TencentNewsSpider
from news.thepaper.thepaper_crawl import ThePaperNewsSpider
from news.toutiao.toutiao_crawl import ToutiaoNewsSpider
from news.weibo.weibo_crawl import WeiBoNewsSpider
from news.sztv.sztv_crawl import SZTVNewsSpider
from argon_log import logger, init_logging

init_logging()

# 定义一个类型别名，表示异步方法
AsyncMethod = Callable[[], Awaitable[None]]

SPIDER_CLASSES = {
    "cctv": CCTVNewsSpider,
    "netease": NeteaseNewsSpider,
    "sina": SinaNewsSpider,
    "tencent": TencentNewsSpider,
    "toutiao": ToutiaoNewsSpider,
    "baidu": BaiduNewsSpider,
    "weibo": WeiBoNewsSpider,
    "the_paper": ThePaperNewsSpider,
    "sztv": SZTVNewsSpider
}

NEWS_METHODS = {
    "hot_news": "fetch_hot_news",
    "latest_china_news": "fetch_latest_china_news",
}


async def run_spider(spider_name: str, news_type: str) -> None:
    """
    根据爬虫名称和新闻类型运行对应的爬虫。

    :param spider_name: 爬虫名称（如 "cctv" 或 "netease"）
    :param news_type: 新闻类型（如 "hot_news" 或 "latest_china_news"）
    :raises ValueError: 如果爬虫名称或新闻类型未知
    """
    spider_class = SPIDER_CLASSES.get(spider_name)
    if not spider_class:
        raise ValueError(f"未知的爬虫名称: {spider_name}")

    method_name = NEWS_METHODS.get(news_type)
    if not method_name:
        raise ValueError(f"未知的新闻类型: {news_type}")

    spider = spider_class()
    method: AsyncMethod = getattr(spider, method_name)
    await method()


async def scheduled_task(spider_name: str, news_type: str, interval: int):
    """
    定时任务：每隔指定时间运行一次爬虫。

    :param spider_name: 爬虫名称
    :param news_type: 新闻类型
    :param interval: 定时任务的间隔时间（单位：分钟）
    """
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        run_spider,
        trigger=IntervalTrigger(minutes=interval),
        args=[spider_name, news_type],
        next_run_time=datetime.now(),  # 立即运行一次
    )
    scheduler.start()
    logger.info(f"定时任务已启动，每隔 {interval} 分钟运行一次爬虫 {spider_name}。")

    try:
        # 保持事件循环运行
        while True:
            await asyncio.sleep(1)
    except (KeyboardInterrupt, SystemExit):
        logger.info("定时任务已停止。")
        scheduler.shutdown()


def main():
    """
    主程序入口：解析命令行参数并启动对应的爬虫或定时任务。
    """
    # 创建命令行参数解析器
    parser = argparse.ArgumentParser(
        description="新闻爬虫主程序",
        epilog="""
            示例：
            命令行模式：python main.py --spider baidu --news-type latest_china_news
                
            参数说明：
            --spider 可选值（爬虫名称）：
                - cctv      （央视新闻）
                - netease   （网易新闻）
                - sina      （新浪新闻）
                - tencent   （腾讯新闻）
                - toutiao   （今日头条）
                - baidu     （百度热榜）
                - thepaper  （澎湃新闻）
                - zhihu     （知乎热榜）
                - weibo     （微博热搜）

            --news-type 可选值（新闻类型）：
                - hot_news            （热点新闻）
                - latest_china_news   （国内最新新闻）
            
            交互模式: 直接运行 python main.py
            """,
    )
    parser.add_argument(
        "--spider",
        type=str,
        required=False,
        choices=[
            "cctv",
            "netease",
            "sina",
            "tencent",
            "toutiao",
            "baidu",
            "weibo",
            "the_paper",
            "sztv"
        ],
        help="指定要运行的爬虫（如 'cctv' 或 'netease'）",
    )
    parser.add_argument(
        "--news-type",
        type=str,
        required=False,
        choices=["hot_news", "latest_china_news"],
        help="指定要抓取的新闻类型（如 'hot_news' 或 'latest_china_news'）",
    )
    parser.add_argument(
        "--interval",
        type=int,
        default=None,
        help="定时任务的间隔时间（单位：分钟）。如果不指定，则只运行一次。",
    )
    args = parser.parse_args()

    # 判断是否进入交互模式
    if not any(vars(args).values()):  # 如果无任何参数
        print("进入交互模式：")
        choices = interactive_menu()
        args.spider = choices["spider"]
        args.news_type = choices["news_type"]
        args.interval = choices["interval"]
    
    # 验证必要参数
    if not args.spider or not args.news_type:
        parser.print_help()
        logger.error(f"爬虫运行失败: {e}")

    # 运行爬虫
    try:
        if args.interval:
            # 启动定时任务
            loop = asyncio.get_event_loop()
            loop.run_until_complete(
                scheduled_task(args.spider, args.news_type, args.interval)
            )
        else:
            # 只运行一次
            loop = asyncio.get_event_loop()
            loop.run_until_complete(run_spider(args.spider, args.news_type))
    except Exception as e:
        logger.error(f"爬虫运行失败: {e}")

def interactive_menu() -> dict[str, str]:
    """交互式菜单选择爬虫和新闻类型"""
    def make_choice(options: list[str], prompt: str) -> str:
        print(f"\n{prompt}:")
        for idx, name in enumerate(options, 1):
            print(f"  {idx}. {name}")
        while True:
            try:
                choice = int(input("请输入编号: ")) - 1
                if 0 <= choice < len(options):
                    return options[choice]
                print(f"错误：请输入1~{len(options)}之间的数字")
            except ValueError:
                print("错误：请输入数字")

    # 选择爬虫
    spider = make_choice(
        list(SPIDER_CLASSES.keys()), 
        "请选择新闻平台"
    )
    
    # 选择新闻类型
    news_type = make_choice(
        list(NEWS_METHODS.keys()), 
        "请选择新闻类型"
    )
    
    # 询问是否定时运行
    interval = None
    if input("\n是否启用定时任务？(y/N): ").lower() == 'y':
        while True:
            try:
                interval = int(input("请输入间隔时间(分钟): "))
                break
            except ValueError:
                print("错误：请输入整数")

    return {"spider": spider, "news_type": news_type, "interval": interval}

import json
import os

def search_news_from_file():
    """
    从本地json文件读取新闻并检索关键词。
    :param spider_name: 爬虫名称（如 netease、sztv）
    :param keyword: 检索关键词
    :return: 匹配的新闻列表
    """
    spider = input("请输入要检索的新闻源（如 netease、sztv）: ").strip()
    keyword = input("请输入要检索的关键词: ").strip()
    if spider and keyword:
        file_path = os.path.join("NewsCrawler", "data", f"{spider}", f"{spider}.json")
        if not os.path.exists(file_path):
            print(f"未找到 {file_path}，请先运行爬虫保存数据。")
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            news_list = json.load(f)

        result = []
        for news in news_list:
            if keyword in news.get("title", "") or keyword in news.get("content", ""):
                result.append(news)
        print(f"共找到{len(result)}条包含“{keyword}”的新闻：")
        for index, news in enumerate(result, start=1):
            print(f"新闻 {index}:")
            print("Title:", news["title"])
            print("URL:", news.get("url", ""))       
if __name__ == "__main__":
    main()
    # 检索功能示例
    search_news_from_file()