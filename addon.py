import xbmcaddon
import xbmcgui
import xbmcplugin
from resources.lib.vier import Vier

import sys
if (sys.version_info[0] == 3):
    # For Python 3.0 and later
    from urllib.parse import urlencode
    from urllib.parse import parse_qsl
else:
    # Fall back to Python 2's urllib2
    from urllib import urlencode
    from urlparse import parse_qsl


PLUGIN_NAME = 'vier'
PLUGIN_ID = 'plugin.video.vier'

_url = sys.argv[0]
_handle = int(sys.argv[1])

_addon = xbmcaddon.Addon()

login_username = xbmcplugin.getSetting(_handle, "username")
login_password = xbmcplugin.getSetting(_handle, "password")
vier = Vier(login_username, login_password)


# het in elkaar klussen van een url welke weer gebruikt word bij router
def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def setMediaView():
    # juiste skin selecteren alleen voor confluence maar die gebruikik prive nog steeds
    try:
        kodiVersion = xbmc.getInfoLabel('System.BuildVersion').split()[0]
        kodiVersion = kodiVersion.split('.')[0]
        skinTheme = xbmc.getSkinDir().lower()
        if 'onfluence' in skinTheme:
            xbmc.executebuiltin('Container.SetViewMode(504)')
    except:
        pass

def list_programmas():
    xbmcplugin.setPluginCategory(_handle, 'Programma\'s op Vier')
    xbmcplugin.setContent(_handle, 'videos')
    programmas = vier.getProgrammas()
    for programma in programmas:
        list_item = xbmcgui.ListItem(label=programma['label'])
        list_item.setInfo('video', programma['video'])
        url = get_url(action='get_episodes', programma_link=programma['programma_link'], programma_naam=programma['label'])
        is_folder = True
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(_handle)

def list_episodes(programma_link, programma_naam):
    xbmcplugin.setPluginCategory(_handle, 'Episodes van %s' % programma_naam)
    xbmcplugin.setContent(_handle, 'videos')
    episodes = vier.getEpisodes(programma_link)
    for episode in episodes:
        list_item = xbmcgui.ListItem(label=episode['label'])
        list_item.setArt(episode['art'])
        list_item.setInfo('video', episode['video'])
        list_item.setProperty('IsPlayable', 'true')
        url = get_url(action='video', video_link=episode['video_link'], videoUuid=episode['videoUuid'])
        is_folder = False
        xbmcplugin.addDirectoryItem(_handle, url, list_item, is_folder)
    xbmcplugin.endOfDirectory(_handle)

def play_video(video_link, videoUuid):
    url = vier.getPlayUrl(video_link, videoUuid)
    playitem = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(_handle, True, listitem=playitem)

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'get_episodes':
            list_episodes(params['programma_link'], params['programma_naam'])
            setMediaView()
        elif params['action'] == 'video':
            play_video(params['video_link'], params['videoUuid'])
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        list_programmas()
        setMediaView()

if __name__ == '__main__':
    router(sys.argv[2][1:])
