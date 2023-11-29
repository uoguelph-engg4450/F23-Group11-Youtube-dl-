# coding: utf-8
from __future__ import unicode_literals

import re

from .common import InfoExtractor
from ..utils import (
    ExtractorError,
    int_or_none,
)


class TelegramIE(InfoExtractor):
    def __init__(self, *args, **kwargs):
        super(TelegramIE, self).__init__(*args, **kwargs)

    _VALID_URL = r'https://t\.me/(?P<user>[^/]+)/(?P<id>\d+)'
    _TEST = {
        'url': 'https://t.me/telegram/165',
        'info_dict': {
            'id': '165',
            'ext': 'mp4',
            'title': 'telegram',
            'description': 'Telegram’s latest update adds a new way to easily create animated stickers from video files.\n\nJanuary Features: 1 • 2 • 3 • More',
            'duration': 13,
        },
    }

    def _real_extract(self, url):
        video_id = self._match_id(url)
        m = re.match(r'https://t\.me/(?P<channel>[^/]+)/', url)
        if m is None:
            raise ExtractorError('Unable to find channel name')
        title = m.group('channel')
        embed_url = url + '?embed=1&mode=tme'
        html = self._download_webpage(embed_url, video_id)

        video_url = self._search_regex(r'<video src="([^"]+)"', html, 'video_url')
        formats = [{'url': video_url, 'ext': 'mp4'}]  # Set the file extension in the 'formats' list

        duration = self._search_regex(
            r'<time class="message_video_duration.*?>(\d+:\d+)<', html,
            'duration', fatal=False)
        if duration:
            try:
                mins, secs = duration.split(':')
                secs = int_or_none(secs)
                mins = int_or_none(mins)
                duration = None if secs is None or mins is None else secs + 60 * mins
            except ValueError:
                duration = None

        description = self._html_search_regex(
            r'<div class="tgme_widget_message_text.*?>(.+?)</div>', html,
            'description', fatal=False)

        return {
            'id': video_id,
            'title': title,
            'description': description,
            'duration': duration,
            'formats': formats
        }

    def extract_info(self, url, download=True):
        return self._real_extract(url)