import os
import time
import bing_crawler as bc


def crawler(keyword):
    # 起始 i=1 每页35张图片
    for i in range(1, 1000 ,35):
        url = bc.getURL(keyword, i)
        print(f"起始{i}: {url}")
        page = bc.requestURL(url)
        data = bc.getData(page)

        for item in data:
            title = item['title']
            keywordlist = bc.getKeyWord(title, keyword)
            if len(keywordlist) != 0:
                filename = keywordlist[0]
            else:
                print("无法定位关键词, 跳过")
                continue
            img_url = item['img']
            if os.path.exists(f"imgs/{keyword}"):
                pass
            else:
                os.mkdir(f"imgs/{keyword}/")
            bc.saveImg(img_url, f"imgs/{keyword}/" + filename + ".jpg")
            time.sleep(1)
        time.sleep(5)


if __name__ == '__main__':
    crawler("消防车")
