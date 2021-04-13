from typing import List

from promnesia.common import extract_urls, Url

# extract urls that look like web links, ignore anything else
def extract_urls_http(s: str) -> List[Url]:
    return list(filter(lambda u: u.startswith("http"), extract_urls(s)))
