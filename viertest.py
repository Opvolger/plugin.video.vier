import html
import sys, re

from resources.lib.vier import Vier

if (sys.version_info[0] == 3):
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
    from urllib.parse import urlencode
else:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request
    from urllib import urlencode

vier = Vier()

print(vier.getProgrammas())

print(vier.getEpisodes("/expeditie-robinson"))

print(vier.getPlayUrl("/video/expeditie-robinson/bekijk-hier-de-eerste-beelden-van-expeditie-robinson-2020"))

def get_webpage(url, data=None):
    req = Request(url)
    req.add_header(
        'User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0')
    req.add_header('Content-Type', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
    response = urlopen(req, data)
    html = response.read().decode("utf-8")
    response.close()
    return html

print('\n programmas \n')

url = 'https://www.vier.be/programmas'

html_page = get_webpage(url)

# print(html)
regex = r"<a class=\"program-overview__link\" href=\"([A-z\/]*)\">([#A-z\s]*)<\/a>"

matches = re.finditer(regex, html_page, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    header = match.group()
    print(match.group(0))
    print(match.group(1))
    print(match.group(2))

print('\n afleveringen \n')

url = 'https://www.vier.be%s' % "/expeditie-robinson"

html_page = get_webpage(url)

regex = r"(https:[A-z=;&\.\-\?\/0-9]*)\" href=\"(\/video[A-z\-\/0-9]*)"

matches = re.finditer(regex, html_page, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    header = match.group()
    # vreemd dat unescape moet...
    print(html.unescape(match.group(0)))
    print(html.unescape(match.group(1)))
    print(html.unescape(match.group(2)))

print('\n video ophalen \n')

url = 'https://www.vier.be%s' % "/video/expeditie-robinson/bekijk-hier-de-eerste-beelden-van-expeditie-robinson-2020"

html_page = get_webpage(url)

regex = r"(https:)([A-z\.0-9\_\/\-]*)(m3u8)"

matches = re.finditer(regex, html_page, re.MULTILINE)

for matchNum, match in enumerate(matches, start=1):
    header = match.group()
    # vreemd dat unescape moet...
    print(html.unescape(match.group(0)))
    print(html.unescape(match.group(1)))
    print(html.unescape(match.group(2)))
