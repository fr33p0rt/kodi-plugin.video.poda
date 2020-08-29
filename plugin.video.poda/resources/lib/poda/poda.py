# -*- coding: utf-8 -*-
# Author/Copyright: fr33p0rt (fr33p0rt@protonmail.com)
# License GPLv3 https://www.gnu.org/copyleft/gpl.html

import requests
import json
import fnmatch

from ..cfg.cfg import Filter

class Poda:

    URL = 'https://live.poda.tv/'
    URL_CHANNELS = 'https://live.poda.tv/api/getSources'
    URL_LOGO = 'https://red-cache.poda.4net.tv/channel/logo/{}.png'
    URL_PAIR = 'https://live.poda.tv/unsecured-api/pairBrowserByPairingCode/'
    URL_DEVICE = 'https://live.poda.tv/api/getDeviceSettings/'
    cookies = None
    channels = []

    def pair(self, pair_code, verify_ssl):
        payload = '{{"id_brand": 1, "pairing_code": "{}", "name": "LiveWeb TV"}}'.format(pair_code)
        print(payload)
        r1 = requests.post(self.URL_PAIR, headers={'Referer': self.URL, 'Content-type': 'application/json'},
                           data=payload, verify=verify_ssl)
        if r1.status_code != 200 or r1.content != '{"success":true,"pairing_success":true}':
            return
        r2 = requests.post(self.URL_DEVICE, headers={'Referer': self.URL, 'Content-type': 'application/json'},
                           cookies=r1.cookies, verify=verify_ssl)
        if r2.status_code != 200 or '"success":true' not in r2.content:
            return

        self.cookies = r2.cookies
        return r2.cookies

    def get_sources_json(self, verify_ssl):
        r = requests.post(self.URL_CHANNELS, cookies=self.cookies, headers={'Referer': self.URL}, verify=verify_ssl)
        return json.loads(r.content)

    def get_channels(self, cfg):
        for i in self.get_sources_json(cfg.verify_ssl)['channels']:
            if (cfg.filter == Filter.SUPPRESS and not any((fnmatch.fnmatchcase(i['name'].encode('utf-8'), f)) for f in cfg.filter_items)) or \
               (cfg.filter == Filter.ONLY and any((fnmatch.fnmatchcase(i['name'].encode('utf-8'), f)) for f in cfg.filter_items)) or \
               cfg.filter == Filter.OFF:
                self.channels.append({'id': str(i['id']), 'name': i['name'], 'img': self.URL_LOGO.format(i['id'])}) #  + str(len(i['content_sources']))
        return self.channels

    def get_stream(self, cfg, ch_id):
        for i in self.get_sources_json(cfg.verify_ssl)['channels']:
            if i['id'] == ch_id:
                return i['content_sources'][0]['stream_profile_urls']['adaptive']

    def set_cookies(self, cookies):
        self.cookies = cookies
