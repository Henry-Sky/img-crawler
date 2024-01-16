import bing_crawler as bc
import re

findKeyWord = re.compile(r'\w{0,2}消防\w{0,3}')

# 关键词: 消防车
url = "https://cn.bing.com/images/search?q=%E6%B6%88%E9%98%B2%E8%BD%A6&form=HDRSC2&first=1"
# 关键词: 国外消防车
url2 = "https://cn.bing.com/images/search?q=%E5%9B%BD%E5%A4%96%E6%B6%88%E9%98%B2%E8%BD%A6&form=HDRSC2&first=1&cw=1513&ch=716"
# 其他
url3 = "https://cn.bing.com/images/search?q=%E6%B6%88%E9%98%B2%E8%BD%A6%E5%96%B7%E6%B0%B4&form=HDRSC2&first=1&cw=1513&ch=716"


page = bc.requestURL(url3)
data = bc.getData(page)

for item in data:
    title = item['title']
    filename = re.findall(findKeyWord, title)[0]
    img_url = item['img']
    if img_url != "":
        bc.saveImg(img_url, "./imgs/" + filename + ".jpg")
        print(f"{filename}: saved")