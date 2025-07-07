import json
from typing import Optional, Any, List, Dict
from argon_log import logger


# 今日头条新闻数据解析器
class ToutiaoNewsDataParser:
    @staticmethod
    def extract_json_from_hot_news(json_str: str) -> Optional[List[Dict[str, Any]]]:
        try:
            json_data = json.loads(json_str)
            news_list = json_data.get("data", [])
            parsed_news = []
            # logger.info(f"{json_data}")
            for news in news_list:
                # logger.info(f"{news}")
                if not isinstance(news, dict):
                    logger.warning("新闻数据格式异常，单条新闻不是字典")
                    continue
                try:
                    # 解析新闻数据
                    parsed_news.append(
                        {
                            "title": news.get("Title", ""),  # 新闻标题
                            "url": news.get("Url", ""),
                        }
                    )
                except Exception as e:
                    logger.warning(f"解析单条新闻数据失败: {e}, 新闻数据: {news}")
                    continue  # 跳过当前新闻，继续解析下一条
            # logger.info(f"{parsed_news}")
            return parsed_news
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败: {e}")
            return None
