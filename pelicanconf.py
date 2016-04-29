#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'Huazai'
SITENAME = u'R_B_prince'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Asia/Harbin'

DEFAULT_LANG = u'en'
LOCALE = ('usa', 'jpn',  # On Windows
    'en_US', 'ja_JP'     # On Unix/Linux
    )
DATE_FORMAT = {
    'en': ('usa','%a, %d %b %Y'),
    'jp': ('jpn','%Y-%m-%d(%a)'),
}

THEME = "blueidea"

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# discuss
PLUGINS = [u"disqus_static"]
DISQUS_SECRET_KEY = u'pJbpiZq4oZnvBF0d8jBAJ7Gq6zgpykrQXz1cb4mu91k9RNy2o4WxBKW1aBGMD0s7'
DISQUS_PUBLIC_KEY = u'lsFpeLT3a3mxbS1P0qlWrhpNfGTiYfXfuMPDLXkbFt2sJke6LXObY01FZSlwD5eb'
DISQUS_SITENAME = u"rbprince"

# Blogroll
LINKS = (('Moseeker', 'http://www.moseeker.com/'),
        )

# Social widget
SOCIAL = (('Facebook', 'https://www.facebook.com/hua.chai.98'),
          ('Twitter', 'https://twitter.com/chaihua483'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True
