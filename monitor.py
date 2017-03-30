import re
import urllib2
import chardet
import urlparse

def crawl_sitemap(url):
    # download the sitemap file
    sitemap = download(url)
    # extract the sitemap links
    links = re.findall('<loc>(.*?)</loc>', sitemap)[1:]
    print links

    #for each site, send links to their site product info checker
    #TrophyRoomCheck(links)

    # download each link
    # for link in links:
    #     # scrape html here
    #     # ...
    #     print link.rsplit('/', 1)[-1]+' '+link
        #html = download(link)



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
    return html


crawl_sitemap('https://shopnicekicks.com/sitemap_products_1.xml')