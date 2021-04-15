from typing import List

from promnesia.common import extract_urls, Url


def _naive_is_url(u: str) -> bool:
    return u.startswith("http") or u.startswith("www.")


# extract urls that look like web links, ignore anything else
def extract_urls_http(s: str) -> List[Url]:
    return list(filter(_naive_is_url, extract_urls(s)))
