# -*- coding: utf-8 -*-
# Module: default
# Author/Copyright: fr33p0rt (fr33p0rt@protonmail.com) (based on code by Roman V. M.)
# License: GPLv3 https://www.gnu.org/copyleft/gpl.html

import sys
from urllib import urlencode
from urlparse import parse_qsl
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon

from resources.lib.cfg.cfg import Cfg
from resources.lib.cfg.cfg import Filter
from resources.lib.cfg import enum34

from resources.lib.poda.poda import Poda

# Get the plugin url in plugin:// notation.
_url = sys.argv[0]
# Get the plugin handle as an integer number.
_handle = int(sys.argv[1])


def get_url(**kwargs):
    """
    Create a URL for calling the plugin recursively from the given set of keyword arguments.

    :param kwargs: "argument=value" pairs
    :type kwargs: dict
    :return: plugin call URL
    :rtype: str
    """
    return '{0}?{1}'.format(_url, urlencode(kwargs))


def list_channels():
    xbmc.log("Reading channels ...", level=xbmc.LOGNOTICE)
    xbmcplugin.setPluginCategory(_handle, 'TV')
    xbmcplugin.setContent(_handle, 'videos')
    for channel in poda.get_channels(cfg):
        list_item = xbmcgui.ListItem(label=channel.get('name'))
        list_item.setArt({'thumb': channel.get('img'),
                          'icon': channel.get('img')})
        list_item.setInfo('video', {'title': channel.get('name'),
                                    'genre': channel.get('name'),
                                    'mediatype': 'video'})
        url = get_url(action='play', id=channel.get('id'))
        list_item.setProperty('IsPlayable', 'true')
        xbmcplugin.addDirectoryItem(_handle, url, list_item, False)
    # Add a sort method for the virtual folder items (alphabetically, ignore articles)
    xbmcplugin.addSortMethod(_handle, xbmcplugin.SORT_METHOD_NONE)
    # Finish creating a virtual folder.
    xbmcplugin.endOfDirectory(_handle)


def play_video(id):
    """
    Play a video by the provided path.

    :param path: Fully-qualified video URL
    :type path: str
    """
    # Create a playable item with a path to play.

    url = poda.get_stream(cfg, int(id))

    xbmc.log(u'Playing channel ...', level=xbmc.LOGNOTICE)
    xbmc.log(str(url), level=xbmc.LOGNOTICE)
    if cfg.verify_ssl:
        play_item = xbmcgui.ListItem(path=url)
    else:
        play_item = xbmcgui.ListItem(path=url + '|verifypeer=false')
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


    # based on example from https://forum.kodi.tv/showthread.php?tid=330507
    # play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
    # play_item.setProperty('inputstream.adaptive.manifest_type', 'mpd')
    # play_item.setMimeType('application/dash+xml')
    # play_item.setContentLookup(False)

    # Pass the item to the Kodi player.
    xbmcplugin.setResolvedUrl(_handle, True, listitem=play_item)


def router(paramstring):
    """
    Router function that calls other functions
    depending on the provided paramstring

    :param paramstring: URL encoded plugin paramstring
    :type paramstring: str
    """
    # Parse a URL-encoded paramstring to the dictionary of
    # {<parameter>: <value>} elements
    xbmc.log(u'Executing PODA plugin ...', level=xbmc.LOGNOTICE)
    params = dict(parse_qsl(paramstring))
    # Check the parameters passed to the plugin
    if params:
        if params['action'] == 'play':
            # Play a video from a provided URL.
            play_video(params['id'])
        else:
            # If the provided paramstring does not contain a supported action
            # we raise an exception. This helps to catch coding errors,
            # e.g. typos in action names.
            raise ValueError('Invalid paramstring: {0}!'.format(paramstring))
    else:
        # If the plugin is called from Kodi UI without any parameters,
        # display the list of video categories
        #list_categories()
        #list_videos('Cars')
        list_channels()


if __name__ == '__main__':
    # Call the router function and pass the plugin call parameters to it.
    # We use string slicing to trim the leading '?' from the plugin call paramstring

    cfg = Cfg()

    cfg.PHPSESSID = xbmcplugin.getSetting(_handle, 'PHPSESSID')
    cfg.device_token = xbmcplugin.getSetting(_handle, 'device_token')

    cfg.filter = Filter(int(xbmcplugin.getSetting(_handle, 'filter')))
    cfg.filter_items = xbmcplugin.getSetting(_handle, 'filter_items').split(',')

    cfg.verify_ssl = xbmcplugin.getSetting(_handle, 'verify_ssl') == 'true'

    poda = Poda()

    pair_code = xbmcplugin.getSetting(_handle, 'pair_code').strip()

    if pair_code:
        cookies = poda.pair(pair_code, cfg.verify_ssl)
        if cookies:
            xbmcaddon.Addon('plugin.video.poda').setSetting(id='pair_code', value='')
            xbmcaddon.Addon('plugin.video.poda').setSetting(id='device_token', value=cookies['device_token'])
            xbmcaddon.Addon('plugin.video.poda').setSetting(id='PHPSESSID', value=cookies['PHPSESSID'])
        else:
            dialog = xbmcgui.Dialog()
            ok = dialog.ok('PODA TV', 'Chyba párování / Pairing error')
            raise Exception('PODA TV - Pairing error')
    else:
        poda.set_cookies({'device_token': cfg.device_token,
                          'PHPSESSID': cfg.PHPSESSID})

    router(sys.argv[2][1:])
