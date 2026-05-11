import requests
from bs4 import BeautifulSoup
import json
import datetime

# 这里是你想抓取的网站地址（先用一个示例，以后可以改）
URL = "https://zb.yfb.qianlima.com/yfbsemsite/mesinfo/zbpglist?source=baidu3&e_matchtype=2&e_creative=136457806852&e_keywordid=1341311794997&bd_vid=11034129572457374220" 

def get_data():
    # 模拟抓取到的数据，以后我们可以根据具体的招标网站修改这里的逻辑
    today = datetime.datetime.now().strftime('%Y-%m-%d')
    new_data = [
        {"title": "VR内容制作", "date": today, "link": "#"},
        {"title": "VR项目", "date": today, "link": "#"},
        {"title": "VR体验", "date": today, "link": "#"}
    ]
    return new_data

# 保存数据到 json 文件
if __name__ == "__main__":
    data = get_data()
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
    print("数据抓取成功！")
