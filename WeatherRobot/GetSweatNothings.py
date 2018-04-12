import requests
from lxml import etree

# 得到网页源代码
def getHtmlText(url):
    kv = {'user-agent': 'Mozilla/5.0'}
    try:
        r = requests.get(url, headers=kv,timeout=30)
        # 如果状态码不是200 则应发HTTPError异常
        r.raise_for_status()
        # 设置正确的编码方式
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "Something Wrong!"

# 解析网页源代码
def parsingHtmlText(html):
    tree = etree.HTML(html)
    note = tree.xpath('//td[@id = "artContent"]//p/text()')
    for sentence in note[1:]:
        print(sentence)
        try:
            withoutNum = sentence.split('.')
            with open('SweetNothings.txt', 'a', encoding=u'utf-8') as f:
                f.write(withoutNum[1] + '\n')
        except:
            print('0')


url = 'http://www.360doc.com/content/18/0225/19/4714218_732399111.shtml'
html = getHtmlText(url)
parsingHtmlText(html)
