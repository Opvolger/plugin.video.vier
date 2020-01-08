import html
import sys
import re

if (sys.version_info[0] == 3):
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
else:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request


class Vier:
    def get_webpage(self, url, data=None):
        req = Request(url)
        req.add_header(
            'User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:25.0) Gecko/20100101 Firefox/25.0')
        req.add_header(
            'Content-Type', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9')
        response = urlopen(req, data)
        html = response.read().decode("utf-8")
        response.close()
        return html

    def getProgrammas(self):
        url = 'https://www.vier.be/programmas'
        html_page = self.get_webpage(url)
        regex = r"<a class=\"program-overview__link\" href=\"([A-z\/]*)\">([#A-z\s]*)<\/a>"

        matches = re.finditer(regex, html_page, re.MULTILINE)

        programmaslist = list()
        for matchNum, match in enumerate(matches, start=1):
            # vreemd dat unescape moet...
            naam = html.unescape(match.group(2))
            episode_link = html.unescape(match.group(1))
            programma = {'label': naam,
                         'video_link': episode_link,
                         'video': {
                             'title': naam,
                             'mediatype': 'video'
                         }
                         }
            programmaslist.append(programma)
        return programmaslist

    def getEpisodes(self, programma_link):
        url = 'https://www.vier.be%s' % programma_link
        html_page = self.get_webpage(url)
        regex = r"(https:[A-z=;&\.\-\?\/0-9]*)\" href=\"(\/video[A-z\-\/0-9]*)"
        matches = re.finditer(regex, html_page, re.MULTILINE)
        episodeslist = list()
        for matchNum, match in enumerate(matches, start=1):
            # vreemd dat unescape moet...
            image = html.unescape(match.group(1))
            video_link = html.unescape(match.group(2))
            episode = {'label': video_link,
                       'video_link': video_link,
                       'art': {'thumb': image,
                               'icon':  image,
                               'fanart': image
                               },
                       'video': {
                           'title': video_link,
                           'mediatype': 'video'
                       }
                       }
            episodeslist.append(episode)
        return episodeslist

    def getPlayUrl(self, video_link):
        url = 'https://www.vier.be%s' % video_link
        html_page = self.get_webpage(url)
        regex = r"(https:)([A-z\.0-9\_\/\-]*)(m3u8)"
        matches = re.finditer(regex, html_page, re.MULTILINE)

        for matchNum, match in enumerate(matches, start=1):
            # vreemd dat unescape moet...
            return print(html.unescape(match.group(0)))
