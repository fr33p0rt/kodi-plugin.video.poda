# -*- coding: utf-8 -*-

# This is free and unencumbered software released into the public domain.
#
# For more information, please refer to <https://unlicense.org>
#
# Author/Copyright: fr33p0rt (fr33p0rt@protonmail.com)

from filter import Filter


class Cfg:
    filter = Filter.OFF  # Filter(1)
    filter_items = None
    verify_ssl = True
    device_token = ''
    PHPSESSID = ''