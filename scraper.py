import requests
from bs4 import BeautifulSoup
import json
import datetime

# 1. 优化后的目标网址（可以尝试在网址后直接带上搜索参数，或者抓取后筛选）
TARGET_URL = "https://zb.yfb.qianlima.com/yfbsemsite/mesinfo/zbpglist"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.baidu.com/"
}

# 2. 定义你感兴趣的关键词
KEYWORDS = ["VR内容制作", "VR项目", "虚拟现实", "VR"]

def get_tenders():
    tenders = []
    try:
        # 获取网页
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8'
        
        if response.status_code != 200:
            return [{"title": f"站点访问受限 (Code: {response.status_code})", "date": "-", "link": "#"}]

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 定位信息列表（根据该网站结构，通常在 list 相关的 div 或 li 中）
        # 这里使用了多个可能的选择器以提高成功率
        items = soup.find_all(['div', 'li'], class_=['mes-list-item', 'list-item', 'clearfix'])
        
        for item in items:
            link_tag = item.find('a')
            if link_tag:
                title = link_tag.get_text(strip=True)
                link = link_tag.get('href', '#')
                
                # --- 核心修改：关键词筛选逻辑 ---
                # 检查标题中是否包含我们想要的关键词
                is_match = any(word in title for word in KEYWORDS)
                
                if is_match:
                    # 补全链接
                    if link.startswith('//'):
                        link = "https:" + link
                    elif link.startswith('/'):
                        link = "https://zb.yfb.qianlima.com" + link
                    
                    # 获取日期
                    date_tag = item.find('span') or item.find('em')
                    date_val = date_tag.get_text(strip=True) if date_tag else datetime.datetime.now().strftime('%Y-%m-%d')
                    
                    tenders.append({
                        "title": title,
                        "date": date_val,
                        "link": link
                    })
                    
    except Exception as e:
        print(f"出错啦: {e}")
        tenders = [{"title": f"程序运行异常", "date": "-", "link": "#"}]
    
    return tenders

if __name__ == "__main__":
    results = get_tenders()
    
    # 如果没找到匹配 VR 的内容
    if not results:
        results = [{
            "title": "今日暂无相关的 VR 招标信息", 
            "date": datetime.datetime.now().strftime('%Y-%m-%d'), 
            "link": "#"
        }]
        
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"抓取完成，找到 {len(results)} 条相关信息")
