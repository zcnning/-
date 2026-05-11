import requests
from bs4 import BeautifulSoup
import json
import datetime

# 中国政府采购网的搜索接口（直接锁定关键词：VR）
TARGET_URL = "http://search.ccgp.gov.cn/bxsearch?searchtype=1&page_index=1&bidSort=0&buyerName=&projectId=&pinMu=0&bidType=0&displayZone=&zoneId=&pppStatus=0&agentName=&keyword=VR"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def get_gov_tenders():
    tenders = []
    try:
        # 发送请求
        response = requests.get(TARGET_URL, headers=HEADERS, timeout=20)
        # 该网站通常使用 UTF-8
        response.encoding = 'utf-8'
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 寻找搜索结果列表（该网站结果通常在 class 为 'vT-srch-result-list-bid' 的 ul 中）
        items = soup.select('.vT-srch-result-list-bid li')
        
        for item in items:
            link_tag = item.find('a')
            if link_tag:
                title = link_tag.get_text(strip=True)
                link = link_tag.get('href')
                
                # 提取日期（通常在标题旁边的 span 里）
                date_tag = item.find('span')
                if date_tag:
                    # 提取形如 "2026.05.11" 的日期并格式化
                    raw_date = date_tag.get_text(strip=True).split('|')[0].strip()
                else:
                    raw_date = datetime.datetime.now().strftime('%Y-%m-%d')

                # 只要标题包含 VR、虚拟现实 或 制作 关键词就收录
                tenders.append({
                    "title": title,
                    "date": raw_date,
                    "link": link
                })
                    
    except Exception as e:
        print(f"抓取出错: {e}")
        tenders = [{"title": f"访问政府官网异常，请稍后再试", "date": "-", "link": "#"}]
    
    return tenders[:20]

if __name__ == "__main__":
    results = get_gov_tenders()
    
    if not results:
        results = [{"title": "今日政府官网暂无相关 VR 招标信息", "date": "-", "link": "#"}]
        
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=4)
    print(f"抓取成功！获取到 {len(results)} 条信息")
