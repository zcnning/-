import requests
from bs4 import BeautifulSoup
import json
import datetime

# 搜索关键词列表
SEARCH_KEYWORDS = ["VR", "虚拟现实", "三维建模", "增强现实"]

def get_all_china_vr():
    all_results = []
    
    for kw in SEARCH_KEYWORDS:
        # 构造搜索 URL：这里锁定全中国的招标公告
        url = f"http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&displayZone=&zoneId=&pppStatus=0&agentName=&keyword={kw}"
        
        try:
            response = requests.get(url, timeout=20)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 抓取列表项
            items = soup.select('.vT-srch-result-list-bid li')
            
            for item in items:
                link_tag = item.find('a')
                if link_tag:
                    title = link_tag.get_text(strip=True)
                    link = link_tag.get('href')
                    date_tag = item.find('span')
                    date_str = date_tag.get_text(strip=True).split('|')[0].strip() if date_tag else "未知日期"
                    
                    # 避免重复
                    if not any(res['title'] == title for res in all_results):
                        all_results.append({
                            "title": title,
                            "date": date_str,
                            "link": link,
                            "keyword": kw # 标记是哪个词搜到的
                        })
        except Exception as e:
            print(f"搜索 {kw} 时出错: {e}")

    # 按日期排序（最近的在前）
    all_results.sort(key=lambda x: x['date'], reverse=True)
    return all_results[:50] # 展示最新的50条

if __name__ == "__main__":
    data = get_all_china_vr()
    if not data:
        data = [{"title": "今日全中国暂无相关VR招标", "date": "-", "link": "#"}]
        
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print(f"已更新全中国VR相关招标信息，共 {len(data)} 条")
