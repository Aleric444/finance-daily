import urllib.request
import xml.etree.ElementTree as ET
import json
import re
from datetime import datetime

def fetch_and_save():
    # new RSS 源
    rss_url = "https://www.cnbc.com/id/10000664/device/rss/rss.html"
    
    try:
        # 请求 RSS
        req = urllib.request.Request(rss_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            xml_data = response.read()
            
        root = ET.fromstring(xml_data)
        news_list = []
        
        # 解析 XML
        for item in root.findall('.//item')[:20]: # 只要前20条最新新闻
            title = item.find('title').text if item.find('title') is not None else ''
            link = item.find('link').text if item.find('link') is not None else ''
            pub_date = item.find('pubDate').text if item.find('pubDate') is not None else ''
            description = item.find('description').text if item.find('description') is not None else ''
            
            # 清洗 HTML 标签
            description = re.sub(r'<[^>]+>', '', description).strip()
            if not description:
                description = "点击跳转至原新闻页面查看详细报道..."
                
            # 格式化时间
            try:
                # 转换 RSS 的时间格式 (例如: Wed, 10 Jun 2026 12:00:00 +0800)
                dt = datetime.strptime(pub_date.split(' +')[0], '%a, %d %b %Y %H:%M:%S')
                time_str = dt.strftime('%H:%M')
            except:
                time_str = "刚刚"

            news_list.append({
                "title": title,
                "link": link,
                "description": description,
                "time": time_str
            })
            
        # 写入本地文件
        with open('news.json', 'w', encoding='utf-8') as f:
            json.dump(news_list, f, ensure_ascii=False, indent=4)
        print("新闻数据更新成功！")
        
    except Exception as e:
        print(f"更新失败: {e}")

if __name__ == "__main__":
    fetch_and_save()
