import validators
from urllib.parse import urlparse
from bs4 import BeautifulSoup


def is_valid_url(url):
    if len(url) > 255:
        return 'URL превышает 255 символов'
    elif validators.url(url) is not True:
        return 'Некорректный URL'
    return None


def normalize_url(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}"


def parse_response(r):
    r.raise_for_status()
    status_code = r.status_code
    htm_text = r.text
    parsed_html = BeautifulSoup(htm_text, "html.parser")
    h1 = parsed_html.h1.get_text().strip() if parsed_html.h1 else ""
    title = (parsed_html.title.string.strip()
             if parsed_html.title else ""
             )
    description_meta = parsed_html.find(
        'meta', attrs={'name': 'description'}
    )
    description = (
        description_meta["content"].strip()
        if description_meta and "content" in description_meta.attrs
        else ""
    )
    return [status_code, h1, title, description]