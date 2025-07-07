import requests
from bs4 import BeautifulSoup

def crawl_page_to_markdown(url, md_filename):
    """
    爬取指定网页的所有内容，并保存为Markdown文件
    :param url: 目标网页地址
    :param md_filename: 保存的Markdown文件名
    """
    response = requests.get(url)
    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, 'html.parser')

    # 提取正文内容（可根据实际网页结构调整）
    # 这里简单提取body标签下的所有文本
    content = soup.body.get_text(separator='\n', strip=True)

    # 也可以直接保存整个HTML为Markdown格式（简单处理）
    # content = soup.prettify()

    with open(md_filename, 'w', encoding='utf-8') as f:
        f.write(f'# {soup.title.string if soup.title else "网页内容"}\n\n')
        f.write(content)

    print(f'爬取完成，内容已保存到{md_filename}')

# 示例调用
if __name__ == '__main__':
    crawl_page_to_markdown('https://api.istero.com/resource/v1/cctv/china/latest/news', 'result.md')