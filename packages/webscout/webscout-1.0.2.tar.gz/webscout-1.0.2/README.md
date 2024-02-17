Search for words, documents, images, videos, news, maps and text translation using the DuckDuckGo.com search engine. Downloading files and images to a local hard drive.

**⚠️ Warning: use AsyncDDGS in asynchronous code**

## Table of Contents
- [Table of Contents](#table-of-contents)
- [Install](#install)
- [CLI version](#cli-version)
- [Duckduckgo search operators](#duckduckgo-search-operators)
- [Regions](#regions)
- [DDGS and AsyncDDGS classes](#ddgs-and-asyncddgs-classes)
- [Exceptions](#exceptions)
- [1. text() - text search by duckduckgo.com](#1-text---text-search-by-duckduckgocom)
- [2. answers() - instant answers by duckduckgo.com](#2-answers---instant-answers-by-duckduckgocom)
- [3. images() - image search by duckduckgo.com](#3-images---image-search-by-duckduckgocom)
- [4. videos() - video search by duckduckgo.com](#4-videos---video-search-by-duckduckgocom)
- [5. news() - news search by duckduckgo.com](#5-news---news-search-by-duckduckgocom)
- [6. maps() - map search by duckduckgo.com](#6-maps---map-search-by-duckduckgocom)
- [7. translate() - translation by duckduckgo.com](#7-translate---translation-by-duckduckgocom)
- [8. suggestions() - suggestions by duckduckgo.com](#8-suggestions---suggestions-by-duckduckgocom)

## Install
```python
pip install -U webscout
```

## CLI version

```python3
python -m webscout --help
```

CLI examples:
[Go To TOP](#TOP)

## Duckduckgo search operators

| Keywords example |	Result|
| ---     | ---   |
| cats dogs |	Results about cats or dogs |
| "cats and dogs" |	Results for exact term "cats and dogs". If no results are found, related results are shown. |
| cats -dogs |	Fewer dogs in results |
| cats +dogs |	More dogs in results |
| cats filetype:pdf |	PDFs about cats. Supported file types: pdf, doc(x), xls(x), ppt(x), html |
| dogs site:example.com  |	Pages about dogs from example.com |
| cats -site:example.com |	Pages about cats, excluding example.com |
| intitle:dogs |	Page title includes the word "dogs" |
| inurl:cats  |	Page url includes the word "cats" |

[Go To TOP](#TOP)

## Regions
<details>
  <summary>expand</summary>

    xa-ar for Arabia
    xa-en for Arabia (en)
    ar-es for Argentina
    au-en for Australia
    at-de for Austria
    be-fr for Belgium (fr)
    be-nl for Belgium (nl)
    br-pt for Brazil
    bg-bg for Bulgaria
    ca-en for Canada
    ca-fr for Canada (fr)
    ct-ca for Catalan
    cl-es for Chile
    cn-zh for China
    co-es for Colombia
    hr-hr for Croatia
    cz-cs for Czech Republic
    dk-da for Denmark
    ee-et for Estonia
    fi-fi for Finland
    fr-fr for France
    de-de for Germany
    gr-el for Greece
    hk-tzh for Hong Kong
    hu-hu for Hungary
    in-en for India
    id-id for Indonesia
    id-en for Indonesia (en)
    ie-en for Ireland
    il-he for Israel
    it-it for Italy
    jp-jp for Japan
    kr-kr for Korea
    lv-lv for Latvia
    lt-lt for Lithuania
    xl-es for Latin America
    my-ms for Malaysia
    my-en for Malaysia (en)
    mx-es for Mexico
    nl-nl for Netherlands
    nz-en for New Zealand
    no-no for Norway
    pe-es for Peru
    ph-en for Philippines
    ph-tl for Philippines (tl)
    pl-pl for Poland
    pt-pt for Portugal
    ro-ro for Romania
    ru-ru for Russia
    sg-en for Singapore
    sk-sk for Slovak Republic
    sl-sl for Slovenia
    za-en for South Africa
    es-es for Spain
    se-sv for Sweden
    ch-de for Switzerland (de)
    ch-fr for Switzerland (fr)
    ch-it for Switzerland (it)
    tw-tzh for Taiwan
    th-th for Thailand
    tr-tr for Turkey
    ua-uk for Ukraine
    uk-en for United Kingdom
    us-en for United States
    ue-es for United States (es)
    ve-es for Venezuela
    vn-vi for Vietnam
    wt-wt for No region
___
</details>

[Go To TOP](#TOP)


## DDGS and AsyncDDGS classes

The DDGS and AsyncDDGS classes are used to retrieve search results from DuckDuckGo.com.
To use the AsyncDDGS class, you can perform asynchronous operations using Python's asyncio library.
To initialize an instance of the DDGS or AsyncDDGS classes, you can provide the following optional arguments:
```python3
class DDGS:
    """webscout class to get search results from duckduckgo.com

    Args:
        headers (dict, optional): Dictionary of headers for the HTTP client. Defaults to None.
        proxies (Union[dict, str], optional): Proxies for the HTTP client (can be dict or str). Defaults to None.
        timeout (int, optional): Timeout value for the HTTP client. Defaults to 10.
    """
```

Here is an example of initializing the DDGS class:
```python3
from webscout import DDGS

with DDGS() as ddgs:
    results = [r for r in ddgs.text("python programming", max_results=5)]
    print(results)
```
Here is an example of initializing the AsyncDDGS class:
```python3
import asyncio
import logging
import sys
from itertools import chain
from random import shuffle

import requests
from webscout import AsyncDDGS

# bypass curl-cffi NotImplementedError in windows https://curl-cffi.readthedocs.io/en/latest/faq/
if sys.platform.lower().startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

def get_words():
    word_site = "https://www.mit.edu/~ecprice/wordlist.10000"
    resp = requests.get(word_site)
    words = resp.text.splitlines()
    return words

async def aget_results(word):
    async with AsyncDDGS(proxies=proxies) as ddgs:
        results = [r async for r in ddgs.text(word, max_results=None)]
        return results

async def main():
    words = get_words()
    shuffle(words)
    tasks = []
    for word in words[:10]:
        tasks.append(aget_results(word))
    results = await asyncio.gather(*tasks)
    print(f"Done")
    for r in chain.from_iterable(results):
        print(r)
    

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
```
It is important to note that the DDGS and AsyncDDGS classes should always be used as a context manager (with statement).
This ensures proper resource management and cleanup, as the context manager will automatically handle opening and closing the HTTP client connection.

## Exceptions

Exceptions:
- `DuckDuckGoSearchException`: Raised when there is a generic exception during the API request.


## 1. text() - text search by duckduckgo.com

```python
from webscout import DDGS

with DDGS() as ddgs:
    for r in ddgs.text('live free or die', region='wt-wt', safesearch='off', timelimit='y', max_results=10):
        print(r)

# Searching for pdf files
with DDGS() as ddgs:
    for r in ddgs.text('russia filetype:pdf', region='wt-wt', safesearch='off', timelimit='y', max_results=10):
        print(r)
```

## 2. answers() - instant answers by duckduckgo.com

```python
from webscout import DDGS

with DDGS() as ddgs:
    for r in ddgs.answers("sun"):
        print(r)
```

## 3. images() - image search by duckduckgo.com

```python
from webscout import DDGS

with DDGS() as ddgs:
    keywords = 'butterfly'
    ddgs_images_gen = ddgs.images(
      keywords,
      region="wt-wt",
      safesearch="off",
      size=None,
      color="Monochrome",
      type_image=None,
      layout=None,
      license_image=None,
      max_results=100,
    )
    for r in ddgs_images_gen:
        print(r)
```

## 4. videos() - video search by duckduckgo.com

```python
from webscout import DDGS

with DDGS() as ddgs:
    keywords = 'tesla'
    ddgs_videos_gen = ddgs.videos(
      keywords,
      region="wt-wt",
      safesearch="off",
      timelimit="w",
      resolution="high",
      duration="medium",
      max_results=100,
    )
    for r in ddgs_videos_gen:
        print(r)
```

## 5. news() - news search by duckduckgo.com

```python
from webscout import DDGS

with DDGS() as ddgs:
    keywords = 'holiday'
    ddgs_news_gen = ddgs.news(
      keywords,
      region="wt-wt",
      safesearch="off",
      timelimit="m",
      max_results=20
    )
    for r in ddgs_news_gen:
        print(r)
```


## 6. maps() - map search by duckduckgo.com

```python
from webscout import DDGS

with DDGS() as ddgs:
    for r in ddgs.maps("school", place="anantnag", max_results=50):
        print(r)
```


## 7. translate() - translation by duckduckgo.com

```python
from webscout import DDGS

with DDGS() as ddgs:
    keywords = 'school'
    r = ddgs.translate(keywords, to="de")
    print(r)
```

## 8. suggestions() - suggestions by duckduckgo.com
```python3
from webscout import DDGS

with DDGS() as ddgs:
    for r in ddgs.suggestions("fly"):
        print(r)
```
