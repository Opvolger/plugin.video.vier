import sys
import re
import json
import requests
from awsidp import AwsIdp
from datetime import datetime

if (sys.version_info[0] == 3):
    # For Python 3.0 and later
    from urllib.request import urlopen, Request
    from html.parser import HTMLParser
    html = HTMLParser()
else:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen, Request
    import HTMLParser
    html = HTMLParser.HTMLParser()


class Vier:
    def __init__(self, login_username, login_password):
        if login_username is not "":
            USER_POOL_ID = "eu-west-1_dViSsKM5Y"
            CLIENT_ID = "6s1h851s8uplco5h6mqh1jac8m"
            self.client = AwsIdp(USER_POOL_ID, CLIENT_ID)
            self.id_token, self.refresh_token = self.client.authenticate(login_username, login_password)

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
        regex = r"<a class=\"program-overview__link\" href=\"([A-z\-\/]*)\">[\n\r\s]*<span[\w\s\d\=\;\:\#\&\.\-\?\/\"]*>[\n\r\s]*([\w\s\d\=\;\:\#\&\.\-\?\/]*)[\n\r\s]*"

        matches = re.finditer(regex, html_page, re.MULTILINE)

        programmaslist = list()
        for matchNum, match in enumerate(matches, start=1):
            # vreemd dat unescape moet...
            naam = html.unescape(match.group(2))
            programma_link = html.unescape(match.group(1))
            programma = {'label': naam.strip().rstrip("\n"),
                         'programma_link': programma_link.strip(),
                         'video': {
                             'title': naam,
                             'mediatype': 'video'
                         }
                         }
            programmaslist.append(programma)
        return programmaslist

    @staticmethod
    def getRegexUitgelicht():
        return r"image=\"([\w\s\d=;:&\.\-\?\/]*)\" href=\"(\/video[\w\s\d=;:&\.\-\?\/]*)\"([\"\s\w\s\d\=><\-\/]*)<h3 class=\"image-teaser__title\">([\w\s\d].*)<\/h3>"

    @staticmethod
    def getRegexEpisodes():        
        return r"href=\"(\/video[\w\s\d=;:&\.\-\?\/]*)\"[\sA-z0-9\=\"><\-]*data-background-image=\"(https:\/\/[a-z0-9\?\=\&;\.\/\-]*)[A-z0-9\=\-\/:!\?#\"<>\s]*data-videoid=\"([a-z0-9\-]*)\"[A-z0-9\=\-\/:!\?#\"<>\s]*<span>([A-z0-9!\s\?\&\;,]*)"

    @staticmethod
    def getJsonEpisodes():
        return r"data-hero=\"([\&\{\w\;\:\-\,\s\.\!\\\/\?\=\}\[\]\@]*)\""

    def getEpisodes(self, programma_link):        
        episodeslist = list()
        url = 'https://www.vier.be%s' % programma_link
        html_page = self.get_webpage(url)


        # json-data
        regex = Vier.getJsonEpisodes()
        matches = re.finditer(regex, html_page, re.MULTILINE)
        
        json_string = None

        for matchNum, match in enumerate(matches, start=1):
            # unescape moet...
            json_string = html.unescape(match.group(1))

        if json_string:
            json_data = json.loads(json_string)
            # deze array moet nog een loop worden
            for episode in json_data['data']['playlists'][0]['episodes']:
                image = html.unescape(episode['image'])
                label = episode['title']
                video_link = episode['link']
                videoUuid = episode['videoUuid']
                episode = {'label': label,
                        'video_link': video_link,
                        'videoUuid': videoUuid,
                        'art': {'thumb': image,
                                'icon':  image,
                                'fanart': image
                                },
                        'video': {
                            'title': label,
                            'plot': episode['pageInfo']['description'],
                            'studio': episode['pageInfo']['site'],
                            'duration': episode['duration'],
                            'premiered': datetime.fromtimestamp(episode['pageInfo']['publishDate']).strftime("%Y-%m-%d"),
                            'aired': datetime.fromtimestamp(episode['pageInfo']['publishDate']).strftime("%Y-%m-%d"),
                            'year': datetime.fromtimestamp(episode['pageInfo']['publishDate']).strftime("%Y"),
                            'mediatype': 'video'
                        }
                        }
                episodeslist.append(episode)                


        # uitgelicht (niet meer getest, dus uit!)
        # regex = Vier.getRegexUitgelicht()
        # matches = re.finditer(regex, html_page, re.MULTILINE)
        
        # for matchNum, match in enumerate(matches, start=1):
        #     # unescape moet...
        #     image = html.unescape(match.group(1))
        #     video_link = html.unescape(match.group(2))
        #     videoUuid = None
        #     label = html.unescape(match.group(4))
        #     episode = {'label': label,
        #                'video_link': video_link,
        #                'videoUuid': videoUuid,
        #                'art': {'thumb': image,
        #                        'icon':  image,
        #                        'fanart': image
        #                        },
        #                'video': {
        #                    'title': label,
        #                    'mediatype': 'video'
        #                }
        #                }
        #     episodeslist.append(episode)

        # de rest
        regex = Vier.getRegexEpisodes()
        matches = re.finditer(regex, html_page, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            # unescape moet...
            video_link = html.unescape(match.group(1))            
            image = html.unescape(match.group(2))
            videoUuid = html.unescape(match.group(3))
            label = html.unescape(match.group(4))
            episode = {'label': label,
                       'video_link': video_link,
                       'videoUuid': videoUuid,
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

    def getPlayUrl(self, video_link, videoUuid):
        if videoUuid:
            self.id_token = self.client.renew_token(self.refresh_token)
            video_link_url = "https://api.viervijfzes.be/content/%s" % videoUuid
            headers = {
                "Authorization": self.id_token,
                "user-agent": "Mozilla/5.0 (Windows; U; Windows NT 6.1; en-GB; rv:1.9.2.13) Gecko/20101203 Firefox/3.6.13 (.NET CLR 3.5.30729)"
            }            
            get_link = requests.get(video_link_url, headers=headers)
            get_json = json.loads(get_link.content)
            return get_json['video']['S']
        url = 'https://www.vier.be%s' % video_link
        html_page = self.get_webpage(url)
        regex = r"(https:[\w\s\d\=\;\:\&\.\-\?\/]*m3u8)"
        matches = re.finditer(regex, html_page, re.MULTILINE)
        for matchNum, match in enumerate(matches, start=1):
            # vreemd dat unescape moet...
            return html.unescape(match.group(1))
        # helaas niks gevonden
