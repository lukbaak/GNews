import hashlib
import json
import logging
import re

from gnews.utils.constants import AVAILABLE_COUNTRIES, AVAILABLE_LANGUAGES


def lang_mapping(lang):
    return AVAILABLE_LANGUAGES.get(lang)


def country_mapping(country):
    return AVAILABLE_COUNTRIES.get(country)


def process_url(item, exclude_websites, proxies=None):
    source = item.get('source').get('href')
    if not all([not re.match(website, source) for website in
                [f'^http(s)?://(www.)?{website.lower()}.*' for website in exclude_websites]]):
        return
    # Google News RSS links are always news.google.com wrapper URLs.  We used
    # to fire a requests.head() here to chase a redirect, but Google stopped
    # issuing HTTP redirects in response to HEAD requests.  The call always
    # failed silently and returned the original wrapper URL unchanged, wasting
    # ~200 ms per article.  Callers that need the real article URL should
    # decode the wrapper URL themselves (e.g. via googlenewsdecoder).
    return item.get('link')
