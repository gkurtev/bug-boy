import os, ssl, re, html

try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen


# Regex used
regex_str = r"""

  (?:"|')                               # Start newline delimiter

  (
    ((?:[a-zA-Z]{1,10}://|//)           # Match a scheme [a-Z]*1-10 or //
    [^"'/]{1,}\.                        # Match a domainname (any character + dot)
    [a-zA-Z]{2,}[^"']{0,})              # The domainextension and/or path

    |

    ((?:/|\.\./|\./)                    # Start with /,../,./
    [^"'><,;| *()(%%$^/\\\[\]]          # Next character can't be...
    [^"'><,;|()]{1,})                   # Rest of the characters can't be

    |

    ([a-zA-Z0-9_\-/]{1,}/               # Relative endpoint with /
    [a-zA-Z0-9_\-/]{1,}                 # Resource name
    \.(?:[a-zA-Z]{1,4}|action)          # Rest + extension (length 1-4 or action)
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters

    |

    ([a-zA-Z0-9_\-/]{1,}/               # REST API (no extension) with /
    [a-zA-Z0-9_\-/]{3,}                 # Proper REST endpoints usually have 3+ chars
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters

    |

    ([a-zA-Z0-9_\-]{1,}                 # filename
    \.(?:php|asp|aspx|jsp|json|
         action|html|js|txt|xml)        # . + extension
    (?:[\?|#][^"|']{0,}|))              # ? or # mark with parameters

  )

  (?:"|')                               # End newline delimiter

"""


def collect_endpoints(content, regex_str):
    regex = re.compile(regex_str, re.VERBOSE)
    items = [{"link": m.group(1)} for m in re.finditer(regex, content)]

    # Remove duplication
    all_links = set()
    no_dup_items = []
    for item in items:
        if item["link"] not in all_links:
            all_links.add(item["link"])
            no_dup_items.append(item)
    items = no_dup_items

    return items 

def send_request(url):
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
    q = Request(url)
    q.add_header('User-Agent', user_agent)
    q.add_header('Accept', 'text/html,\
        application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
    q.add_header('Accept-Language', 'en-US,en;q=0.8')
    q.add_header('Accept-Encoding', 'gzip')

    try:
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        response = urlopen(q, timeout=10, context=sslcontext)
    except:
        sslcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
        response = urlopen(q, timeout=10, context=sslcontext)

    if response.info().get('Content-Encoding') == 'gzip':
        data = GzipFile(fileobj=readBytesCustom(response.read())).read()
    elif response.info().get('Content-Encoding') == 'deflate':
        data = response.read().read()
    else:
        data = response.read()

    return data.decode('utf-8', 'replace')

def cli_output(endpoints):
    for endpoint in endpoints:
        print(html.escape(endpoint["link"]).encode(
            'ascii', 'ignore').decode('utf8'))

def start(input):
    try:
        file = send_request(input)
    except Exception as e:
        print('Error comming from {}'.format(e))
    
    endpoints = collect_endpoints(file, regex_str)
    cli_output(endpoints)


if __name__ == "__main__":
    path = "file://{}".format(os.path.abspath("analyzer/page-source-code.txt"))
    start(path)
