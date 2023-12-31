import seleniumwire.undetected_chromedriver as uc
from bs4 import BeautifulSoup
from url_finder import start
from urllib.parse import quote
import os
import hashlib
import os
import subprocess
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global variables
CUSTOM_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
APPLICATION_JSON_DIR = "application-json"
INFO_DIR = "info"
URLS_FILE = "urls.txt"
TARGET_URL = input("Target url: ")
KEY_WORD = input("Key word: ")

if TARGET_URL == "test":
    TARGET_URL = "http://testphp.vulnweb.com/"

print(TARGET_URL)

seleniumwire_options = {
    "proxy": {"https": "https://127.0.0.1:8080", "http": "http://127.0.0.1:8080"}
}

if not os.path.exists("analyzer"):
    os.makedirs("analyzer")

if not os.path.exists(APPLICATION_JSON_DIR):
    os.makedirs(APPLICATION_JSON_DIR)

URL_COLLECTOR_PATH_FULL = os.path.join(INFO_DIR, URLS_FILE)
if not os.path.exists(URL_COLLECTOR_PATH_FULL):
    os.makedirs(INFO_DIR)
    os.mknod(URL_COLLECTOR_PATH_FULL)


def configure_driver():
    # TODO
    # options.add_argument('--headless')
    ## Chrome Options
    options = uc.ChromeOptions()
    options.add_argument("--ignore-ssl-errors=yes")
    options.add_argument("--ignore-certificate-errors")
    driver = uc.Chrome(seleniumwire_options=seleniumwire_options, options=options)
    return driver


def interceptor(request):
    del request.headers["user-agent"]
    # request.headers["user-agent"] = CUSTOM_UA


def interceptor_resp(request, response):
    if request.headers["Content-Type"] == "application/json":
        print(
            f"Request(application/json): {request.method} {request.url} {response.status_code}\n"
        )
        filename = f"{request.method}_{request.url}_{response.status_code}.txt".lower()
        filename = hashlib.md5(filename.encode()).hexdigest()
        path = os.path.join(APPLICATION_JSON_DIR, filename)
        if not os.path.exists(path):
            with open(path, "w") as file:
                # Request and Response objects options
                # Request object
                # body	The request body as bytes. If the request has no body the value of body will be empty, i.e. b''.
                # cert	Information about the server SSL certificate in dictionary format. Empty for non-HTTPS requests.
                # date	The datetime the request was made.
                # headers	A dictionary-like object of request headers.
                # host	The request host, e.g. www.example.com
                # method	The HTTP method, e.g. GET or POST etc.
                # params	A dictionary of request parameters. If a parameter with the same name appears more than once in the request, it's value in the dictionary will be a list.
                # path	The request path, e.g. /some/path/index.html
                # querystring	The query string, e.g. foo=bar&spam=eggs
                # response	The response object associated with the request. This will be None if the request has no response.
                # url	The request URL, e.g. https://www.example.com/some/path/index.html?foo=bar&spam=eggs
                # ----------------------------------------------------------------------------------------
                # Response object
                # body	The request body as bytes. If the request has no body the value of body will be empty, i.e. b''.
                # date	The datetime the request was made.
                # headers	A dictionary-like object of request headers.
                # reason	The reason phrase, e.g. OK or Not Found etc..
                # status_code	The status code of the response, e.g. 200 or 404 etc.
                file.write(f"{request.method} {request.url}\n")
                file.write(f"{request.headers}\n")
                file.write(f"{request.body}\n")
                file.write(f"{request.params}\n\n")
                file.write("==============================\n\n")
                file.write(f"{response.status_code} {response.reason}\n")
                file.write(f"{response.headers}\n")
                file.write(f"{response.body}\n")

def extract_urls(driver):
    html_source = driver.page_source
    soup = BeautifulSoup(html_source, "html.parser")
    with open("analyzer/page-source-code.txt", "w") as file:
        file.write(html_source)
    with open("analyzer/page-source-code-prettified.txt", "w") as file:
        file.write(soup.prettify())
    print("==================Urls extraction start================\n")
    path = "file://{}".format(os.path.abspath("analyzer/page-source-code.txt"))
    start(path, URL_COLLECTOR_PATH_FULL)
    print("==================Urls extraction end================\n")

driver = configure_driver()
driver.request_interceptor = interceptor
driver.response_interceptor = interceptor_resp
driver.get(f"{TARGET_URL}")

# Keep the script running to allow SeleniumWire events to trigger
browser_running = True

while browser_running:
    user_input = input("Actions (extract urls(e)/quit(q)\n")
    if user_input == "e":
        extract_urls(driver)
    elif user_input == "q":
        browser_running = False

driver.quit()
