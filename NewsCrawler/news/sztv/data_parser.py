# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

class SZTVNewsDataParser:
    def parse_news_list(self, html_text):
        """
        解析深圳卫视新闻列表页，返回新闻条目列表。
        :param html_text: 新闻列表页 HTML
        :return: [{'title': ..., 'url': ...}, ...]
        """
        soup = BeautifulSoup(html_text, "html.parser")
        news_list = []
        # 遍历所有新闻条目
        for item in soup.select("div.news-list-more-list div.item_article"):
            a_tag = item.find("a", href=True)
            title_tag = item.select_one("div.item_text")
            if a_tag and title_tag:
                url = a_tag["href"]
                title = title_tag.get_text(strip=True)
                if url and title:
                    news_list.append({"title": title, "url": url})
        return news_list
