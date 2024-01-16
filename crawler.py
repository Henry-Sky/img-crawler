import bing_crawler as bc
import re

findKeyWord = re.compile(r'\w{0,2}消防\w{0,3}')

url = "https://cn.bing.com/images/search?q=%E6%B6%88%E9%98%B2%E8%BD%A6&FORM=HDRSC2"
page = bc.requestURL(url)
data = bc.getData(page)

for item in data:
    title = item['title']
    filename = re.findall(findKeyWord, title)[0]
    img_url = item['img']
    bc.saveImg(img_url, "./imgs/" + filename + ".jpg")