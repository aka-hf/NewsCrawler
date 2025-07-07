# 📰 NewsCrawler

## 🕸️ 仓库描述 🕸️

该仓库是一个新闻爬虫项目，用于从多个新闻源中获取新闻数据,如央视新闻、网易新闻、新浪新闻、腾讯新闻、今日头条、百度新闻等。

## 🚀 功能特性

- **多新闻源支持**：支持从多个主流新闻网站抓取数据。
- **数据存储**：支持将抓取的新闻数据存储到 Mysql 数据库中，支持导出为 CSV 和 JSON 文件。
- **定时任务**：支持定时抓取新闻数据，保持数据更新。
- **钉钉通知**：支持通过钉钉机器人发送抓取新闻。
- **飞书通知**：支持通过飞书机器人发送抓取新闻。

---

## 📊 支持的新闻源

| 网站   | 国内最新新闻 | 热点新闻 |
|------|--------|------|
| 央视新闻 | ✅      | ✅    |热点新闻更全面且涵盖了国内最新新闻
| 网易新闻 | ✅      | ✅    |热点新闻只有官方推荐的十条,国内最新新闻更多
| 新浪新闻 | ❌      | ✅    |只支持热点新闻，爬取50条
| 腾讯新闻 | ❌      | ✅    |只支持热点新闻
| 今日头条 | ❌      | ✅    |只支持热点新闻，返回title、url
| 百度新闻 | ❌      | ✅    |返回title、url和description，其中url为百度检索结果
| 澎湃新闻 | ❌      | ✅    |只支持热点新闻
| 深圳卫视 | ❌      | ✅    |动态网页，爬取速度慢，经常会超时，若是不要求内容只需要URL和title的话可以快些
| 微博   | ❌      | ✅    |只支持热点新闻，返回title和url

---

## 🛠️ 快速开始

### 1. 安装依赖

确保已安装 Python 3.11 或更高版本，然后运行以下命令安装依赖：

```bash
pip install -r requirements.txt
```

或

```bash
poetry install
```

### 3. 运行爬虫

运行以下命令启动指定新闻源的爬虫：

```bash
python NewsCrawler/main.py --spider <spider_name> --news-type <news_type>
```

- **`<spider_name>`**：爬虫名称，可选值：`cctv`、`netease`、`sina`、`tencent`、`toutiao`、`baidu`、`the_paper`、`sztv`、`weibo`。
- **`<news_type>`**：新闻类型，可选值：`hot_news`（热点新闻）或 `latest_china_news`（国内最新新闻）。

#### 启动定时任务

如果需要定时抓取新闻，可以使用 `--interval` 参数指定抓取间隔（单位：分钟）：

```bash
python NewsCrawler/main.py --spider netease --news-type hot_news --interval 10
```





