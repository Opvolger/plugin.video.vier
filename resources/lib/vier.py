import HTMLParser
html = HTMLParser.HTMLParser()

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
        regex = r'<a class="program-overview__link" href="([A-z\-\/]*)">([\w\s\d\=\;\:\#\&\.\-\?\/]*)<\/a>'

        matches = re.finditer(regex, html_page, re.MULTILINE)

        programmaslist = list()
        for matchNum, match in enumerate(matches, start=1):
            # vreemd dat unescape moet...
            naam = html.unescape(match.group(2))
            programma_link = html.unescape(match.group(1))
            programma = {'label': naam,
                         'programma_link': programma_link,
                         'video': {
                             'title': naam,
                             'mediatype': 'video'
                         }
                         }
            programmaslist.append(programma)
        return programmaslist

    @staticmethod
    def getRegexLink():
        # '+Vier.getRegexLink()+r'
        return r'([\w\s\d=;:&\.\-\?\/]*)'

    @staticmethod
    def getRegexLinkVideo():
        return '(\/video[\w\s\d=;:&\.\-\?\/]*)'

    @staticmethod
    def getRegexUitgelicht():
        return r'image="'+Vier.getRegexLink()+r'" href="'+Vier.getRegexLinkVideo()+r'"(["\s\w\s\d\=><\-\/]*)<h3 class="image-teaser__title">([\w\s\d].*)<\/h3>'

    @staticmethod
    def getRegexEpisodes():
        return r'href="'+Vier.getRegexLinkVideo()+r'"([\sA-z0-9\=\"><\-]*)data-background-image="(https:\/\/[a-z0-9\?\=\&;\.\/\-]*)([A-z0-9\=\-\/:!\?#\"<>\s]*)<span>([A-z0-9!\s]*)'

    def getEpisodes(self, programma_link):
        url = 'https://www.vier.be%s' % programma_link
        html_page = self.get_webpage(url)

        # uitgelicht
        regex = Vier.getRegexUitgelicht()
        matches = re.finditer(regex, html_page, re.MULTILINE)
        episodeslist = list()
        for matchNum, match in enumerate(matches, start=1):
            # vreemd dat unescape moet...
            image = html.unescape(match.group(1))
            video_link = html.unescape(match.group(2))
            label = html.unescape(match.group(4))
            episode = {'label': label,
                       'video_link': video_link,
                       'art': {'thumb': image,
                               'icon':  image,
                               'fanart': image
                               },
                       'video': {
                           'title': label,
                           'mediatype': 'video'
                       }
                       }
            episodeslist.append(episode)

        # de rest
        regex = Vier.getRegexEpisodes()
        matches = re.finditer(regex, html_page, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            # vreemd dat unescape moet...
            video_link = html.unescape(match.group(1))
            image = html.unescape(match.group(3))
            label = html.unescape(match.group(5))
            episode = {'label': label,
                       'video_link': video_link,
                       'art': {'thumb': image,
                               'icon':  image,
                               'fanart': image
                               },
                       'video': {
                           'title': label,
                           'mediatype': 'video'
                       }
                       }
            episodeslist.append(episode)

        return episodeslist

    def getPlayUrl(self, video_link):
        url = 'https://www.vier.be%s' % video_link
        html_page = self.get_webpage(url)
        regex = r"(https:[\w\s\d\=\;\:\&\.\-\?\/]*m3u8)"
        matches = re.finditer(regex, html_page, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            # vreemd dat unescape moet...
            return html.unescape(match.group(1))
