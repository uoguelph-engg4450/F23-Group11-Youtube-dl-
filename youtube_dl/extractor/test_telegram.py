import pytest
from youtube_dl.extractor.telegram import TelegramIE
from youtube_dl import YoutubeDL

@pytest.mark.parametrize("url, expected_info_dict", [
    (
        'https://t.me/telegram/165',
        {
            'id': '165',
            'ext': 'mp4',
            'title': 'telegram',
            'description': 'Telegram’s latest update adds a new way to easily create animated stickers from video files.\n\nJanuary Features: 1 • 2 • 3 • More',
            'duration': 13,
        }
    ),
])

def test_telegram_ie(url, expected_info_dict):
    ie = TelegramIE()
    
    downloader = YoutubeDL()
    ie._downloader = downloader
    
    result = ie.extract_info(url, download=False)

    assert result['id'] == expected_info_dict['id']
    assert result['formats'][0]['ext'] == expected_info_dict['ext']
    assert result['title'] == expected_info_dict['title']
    assert result['description'] == expected_info_dict['description']
    assert result['duration'] == expected_info_dict['duration']
