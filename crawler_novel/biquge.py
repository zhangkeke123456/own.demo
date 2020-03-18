import requests
import time
from lxml import etree


def get_chapter(url):
    """
    返回章节列表
    :return chapter list
    """
    print(url)
    kv = {
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.xbiquge.la",
        "Referer": "http://www.xbiquge.la/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/75.0.3770.80 Safari/537.36"
    }

    try:
        print("开始获取章节信息")
        r = requests.get(url=url, headers=kv)
        r.encoding = 'utf-8'
        # print(r.text)

        tree = etree.HTML(r.text)
        node_lists = tree.xpath('//div[@class="box_con"]')

        lists = node_lists[0].xpath('//div[@id="list"]')
        little_urls = lists[0].xpath('//dl/dd/a//@href')
        titles = lists[0].xpath('//dl/dd/a//text()')
        print("结束获取章节信息")
        return [little_urls, titles, len(titles)]

    except Exception as e:
        print("连接失败")

    return None


def get_content(url, book_title, start_page=0):
    url_title_lists = get_chapter(url)

    kv = {
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "www.xbiquge.la",
        "Referer": url,
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/75.0.3770.80 Safari/537.36"
    }

    f = open(r"C:\Users\user\Desktop\%s.txt" % book_title, 'w', encoding='utf-8') if start_page == 0 else \
        open(r"C:\Users\user\Desktop\%s.txt" % book_title, 'a', encoding='utf-8')

    try:
        print('开始下载')
        print(url_title_lists[2])
        if start_page > url_title_lists[2]:
            pass
        else:
            for i in range(start_page, url_title_lists[2]):
                print('章节：' + str(i + 1))
                title = url_title_lists[1][i]
                f.write(title + "\n" if i == 0 else "\n" + title + "\n")
                time.sleep(2)
                single_url = url + url_title_lists[0][i].split('/')[3]

                r = requests.get(single_url, headers=kv)
                r.encoding = 'utf-8'
                tree = etree.HTML(r.text)
                contents = tree.xpath('//div[@id="content"]//text()')
                print("文章获取成功")
                for content in contents:
                    c = content
                    f.write(c)
            print('结束下载')
    except Exception as e:
        print(e)

    f.close()


if __name__ == "__main__":
    url = input("请输入笔趣阁书籍的地址：")
    title = input("请输入书籍名称：")
    get_content(url.strip(), title, start_page=8955)
