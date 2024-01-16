import urllib.request, urllib.error
from bs4 import BeautifulSoup
import re

findTitle = re.compile(r'\"t\":(.*?),')
findNoise = re.compile(r'[, , _, -, |]')

findHref = re.compile(r'href=\"(.*?)\"')
findMurl = re.compile(r'\"murl\":\"(.*?)\",')
findLnkw = re.compile(r'<div class=\"lnkw\">(.*?)</div>')


def requestURL(url):
    # 设置请求标头,伪装成浏览器请求
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0"
    }
    request = urllib.request.Request(url, headers=headers)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


def getData(targethtml):
    soup = BeautifulSoup(targethtml, "html.parser")
    # 对每一条搜索信息标签进行检索
    data = []
    for item in soup.find_all('div', class_="imgpt"):
        item = str(item)
        item_data = {}

        # 网页信息概括
        head_title = re.findall(findTitle, item)[0]
        title = re.sub(findNoise, "", head_title)
        item_data["title"] = title

        # 预览图片链接
        img_src = re.findall(findMurl, item)
        img = [x for x in img_src if x != '']
        item_data["img"] = img[0]

        # 外部链接
        lnkw = re.findall(findLnkw, item)[0]
        href = re.findall(findHref, lnkw)[0]
        item_data["ref"] = str(href)

        # 打包单个搜索数据
        data.append(item_data)
    return data


"""
if __name__ == "__main__":
    url = "https://www.bing.com/images/search?q=%E6%B6%88%E9%98%B2%E8%BD%A6&form=HDRSC2&first=1&cw=1177&ch=701"
    page = requestURL(url)
    data = getData(page)
    print(data)
"""