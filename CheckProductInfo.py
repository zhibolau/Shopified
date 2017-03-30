# coding=utf-8
import re
import urllib2
import chardet
import urlparse
from bs4 import BeautifulSoup
import requests

def download(url, user_agent='wswp', proxy=None, num_retries=2): # download('https://www.google.co.jp/', proxy='127.0.0.1:1080')
    print 'Downloading: ', url.rsplit('/', 1)[-1]+' '+url
    headers = {'User-agent' : user_agent}
    request = urllib2.Request(url, headers=headers)

    opener = urllib2.build_opener()
    if proxy:
        proxy_params = {urlparse.urlparse(url).scheme: proxy}
        opener.add_handler(urllib2.ProxyHandler(proxy_params))
    try:
        html = opener.open(request).read()
        charset = chardet.detect(html)['encoding']
        if charset == 'GB2312' or charset == 'gb2312':
            html = html.decode('GBK').encode('GB18030')
        else:
            html = html.decode(charset).encode('GB18030')
    except urllib2.URLError as e:
        print 'Download error', e.reason
        html = None
        if num_retries > 0:
            if num_retries > 0:
                if hasattr(e, 'code') and 500 <= e.code < 600:
                    # recursively retry 5xx HTTP errors
                    return download(url, user_agent, proxy, num_retries-1)
    print html
    return html

#download the whole html
#download(url,user_agent='wswp', proxy=None, num_retries=2)

# call checkProductInfo时候会传递过来 整个sitemap的url list  ！！！

#shoe status
SOLDOUT = 'SoldOut'
AVAILABLEALL = 'AvailableAll'
SOLDOUTPARTIAL = 'SoldOutPartial'
NEWLYADDED = 'NewlyAdded'
RESTOCK = 'Restock'

#list holds shoes that can be potentially restocked
potentialRestock = []

class Shoe:
    def __init__(self, link, sizePrice, status):
        self.link = link
        self.sizePrice = sizePrice
        self.status = status

# check partial restock
lastSizePrice = sizePrice


#可以加上 stock count， atc link
def checkProductInfo(url):
    #soldout
    #url = 'https://www.trophyroomstore.com/collections/jordan-brand-footwear/products/air-jordan-atmos-pack?variant=31796802194'
    result = requests.get(url)
    c = result.content

    #available
    #urlAvailable = 'https://www.trophyroomstore.com/collections/all/products/air-jordan-4-retro-motorsport'
    # resultAvailable = requests.get(urlAvailable)
    # cAvailable = resultAvailable.content

    soup = BeautifulSoup(c, "lxml")
    select = soup.find("select", { "class" : "product-single__variants" }).findAll("option")

    #find out if the product is available to be added to cart
    # spanAddToCart = soup.find("button",{"id" : "AddToCart"})
    # print spanAddToCart

    sizePrice=[]
    shoe = Shoe(url, sizePrice, "availableNow")
    for s in select:
    #     currentSelect.append(s)
    # print currentSelect
        #print type(s.string)
        #print s.string
        sizePrice.append(str(s.string.replace(' ', '').replace("\n", "")))

    #check if all shoes r sold out
    soldOutCount=0
    for s in sizePrice:
        if 'SoldOut' in s:
            soldOutCount +=1
    if soldOutCount == len(sizePrice): #use is here is also working
        shoe.status = SOLDOUT
    elif soldOutCount == 0:
        shoe.status = AVAILABLEALL
    else:
        shoe.status = SOLDOUTPARTIAL

    print shoe.link
    print shoe.sizePrice
    print shoe.status

#soldout
url = 'https://www.trophyroomstore.com/collections/jordan-brand-footwear/products/air-jordan-atmos-pack?variant=31796802194'
#available
urlAvailable = 'https://www.trophyroomstore.com/collections/all/products/air-jordan-4-retro-motorsport'
urlPartiallyOOS = 'https://www.trophyroomstore.com/collections/jordan-brand/products/air-jordan-6-black'
checkProductInfo(urlPartiallyOOS)