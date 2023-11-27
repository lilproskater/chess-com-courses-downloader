from requests import get
from re import sub as re_sub
from config import COOKIE_HEADER


def get_request(url, host='www.chess.com'):
    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
        'Alt-Used': 'www.chess.com',
        'Connection': 'keep-alive',
        'Host': host,
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Sec-Fetch-User': '?1',
        'TE': 'trailers',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0', 
    }
    if COOKIE_HEADER:
        headers['Cookie'] = COOKIE_HEADER
    return get(url, headers=headers)


def write_file(fname, mode, data, encoding=None):
    with open(fname, mode, encoding=encoding) as f:
        f.write(data)


def read_file(fname, mode='r', encoding=None):
    with open(fname, mode, encoding=encoding) as f:
        data = f.read()
    return data


def image_link_to_fname(link):
    return 'image.' + link.split('.')[-1]


def escape_folder_name(string):
    return re_sub(r'[\?\\\/\:\*\:\<\>\|]', '', string)
