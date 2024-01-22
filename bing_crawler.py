import random
import urllib.request, urllib.error
from bs4 import BeautifulSoup
import re

# HTML中搜寻目标信息的正则匹配式
findTitle = re.compile(r'\"t\":(.*?),')
findNoise = re.compile(r'[, , _, -, |]')
findHref = re.compile(r'href=\"(.*?)\"')
findMurl = re.compile(r'\"murl\":\"(.*?)\",')
findLnkw = re.compile(r'<div class=\"lnkw\">(.*?)</div>')


def getKeyWord(origin, key, before=2, end=3):
    keywordlist = re.findall(re.compile(r"\w{0,"+str(before)+"}"+key+"\w{0,"+str(end)+"}"), origin)
    return keywordlist


def getURL(keyword, first, pagenum=35):
    bin = bytes(keyword, encoding='utf-8').hex()
    index = 0
    res = '%'
    for char in bin:
        index = index + 1
        res += char
        if index % 2 == 0 and index != len(bin):
            res += '%'
    return (
        "https://cn.bing.com/images/search?q=" + res +
        f"&form=HDRSC2&first={first}&count={pagenum}&relp={pagenum}&scenario=ImageBasicHover&datsrc=N_I&layout=RowBased&mmasync=1"
    )

def getheader():
    # 随机请求头
    headers = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
        "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
        "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
        "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)"

    ]
    index = random.randint(0, int(len(headers) - 1))
    return {"User-Agent":headers[index]}


def requestURL(url):
    # 设置请求标头,伪装成浏览器请求
    header = getheader()
    request = urllib.request.Request(url, headers=header)
    response = urllib.request.urlopen(request)
    html = response.read().decode("utf-8")
    return html


def getData(targethtml):
    soup = BeautifulSoup(targethtml, "html.parser")
    # 对每一条搜索信息标签进行检索
    data = []
    for item in soup.find_all('div', class_="imgpt"):
        item = str(item)
        item_data = {}

        # 网页信息概括
        head_title = re.findall(findTitle, item)
        if len(head_title) != 0:
            title = re.sub(findNoise, "", head_title[0])
            item_data["title"] = title
        else:
            print("未找到title, 跳过!")
            continue

        # 预览图片链接
        img_list = re.findall(findMurl, item)
        img = [x for x in img_list if x != '']
        if len(img) != 0:
            item_data["img"] = img[0]
        else:
            print("未发现图片, 跳过!")
            continue

        # 外部链接
        lnkw_list = re.findall(findLnkw, item)
        if len(lnkw_list) != 0:
            href_list = re.findall(findHref, lnkw_list[0])
            if len(href_list) != 0:
                item_data["ref"] = str(href_list[0])
            else:
                print("未找到href, 跳过!")
                continue
        else:
            print("未找到lnkw, 跳过!")
            continue

        # 打包单个搜索数据
        data.append(item_data)
    return data


def saveImg(url, filename):
    header = getheader()
    res = urllib.request.Request(url, headers=header)
    with open(filename, "wb") as f:
        f.write(urllib.request.urlopen(res).read())
        print("保存图片: " + filename)


"""
if __name__ == "__main__":
    url = "https://www.bing.com/images/search?q=%E6%B6%88%E9%98%B2%E8%BD%A6&form=HDRSC2&first=1&cw=1177&ch=701"
    page = requestURL(url)
    data = getData(page)
    print(data)
"""
