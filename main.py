# -*- coding: utf-8 -*-
# Created by KubiszDeny
# Under eNetwork.cz
# NewBuild ver1.3.2
# Stable plugin.video.bombuj.filmyserialy

import sys
from urllib import urlencode
from urlparse import parse_qsl
import xbmc
import xbmcgui
import xbmcplugin
import urllib2
from urllib2 import urlopen
import json
import resolveurl

_url = sys.argv[0]
handle = int(sys.argv[1])

def get_jsonparsed_data(url):
    response = urlopen(url)
    data = response.read()
    return json.loads(data)
url = ("http://kodi.enetwork.cz/source.json")
VIDEOS = get_jsonparsed_data(url)

def get_url(**kwargs):
    return '{0}?{1}'.format(_url, urlencode(kwargs))

def get_categories():
    return VIDEOS.iterkeys()

def get_videos(category):
    return VIDEOS[category]

def list_categories():
    xbmcplugin.setPluginCategory(handle, '[COLOR blue]Hlavní stránka[/COLOR]')
    xbmcplugin.setContent(handle, 'videos')
    categories = get_categories()
    for category in categories:
        list_item = xbmcgui.ListItem(label=category)
        list_item.setArt({'thumb': VIDEOS[category][0]['thumb'],
                          'icon': VIDEOS[category][0]['thumb'],
                          'fanart': VIDEOS[category][0]['thumb']})
        list_item.setInfo('video', {'title': category,
                                    'genre': category,
                                    'mediatype': 'video'})
        url = get_url(action='listing', category=category)
        is_folder = True
        xbmcplugin.addDirectoryItem(handle, url, list_item, is_folder)
    xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(handle)

def list_videos(category):
    xbmcplugin.setPluginCategory(handle, category)
    xbmcplugin.setContent(handle, 'videos')
    videos = get_videos(category)
    for video in videos:
        list_item = xbmcgui.ListItem(label=video['name'])
        list_item.setInfo('video', {'title': video['name'],
                                    'genre': video['genre'],
                                    'mediatype': 'video'})
        list_item.setArt({'thumb': video['thumb'], 'icon': video['thumb'], 'fanart': video['thumb']})
        list_item.setProperty('IsPlayable', 'true')
        url = get_url(action='play', video=video['video'])
        is_folder = False
        xbmcplugin.addDirectoryItem(handle, url, list_item, is_folder)
    xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL_IGNORE_THE)
    xbmcplugin.endOfDirectory(handle)

def play_video(path):
    try:
        resolved_url = resolveurl.resolve(path)
        listitem = xbmcgui.ListItem(path=resolved_url)
        xbmcplugin.setResolvedUrl(handle, True, listitem)
    except:
        play_item = xbmcgui.ListItem(path=path)
        xbmcplugin.setResolvedUrl(handle, True, listitem=play_item)

def router(paramstring):
    params = dict(parse_qsl(paramstring))
    if params:
        if params['action'] == 'listing':
            list_videos(params['category'])
        elif params['action'] == 'play':
            play_video(params['video'])
        else:
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        list_categories()

if __name__ == '__main__':
    line1 = "Doplněk Bombuj.eu"
    line2 = "Tímto Vás vítám v nové verzi doplňku Bombuj.eu. Doplněk je bezplatný, můžete přispět dobrovolnou částkou na bankovní účet 1766873010/3030 (Airbank). Za podporu Vám děkuji."
    line3 = "Na vývoji se můžete podílet i vy! Máte Návrhy nebo nápady na zlepšení? Napište nám na fórum. Nebo na Kodi.eNetwork.cz"

    xbmcgui.Dialog().ok(line1, line2, line3)

    router(sys.argv[2][1:])
