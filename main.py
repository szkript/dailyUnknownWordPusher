from requests import get
from requests.exceptions import RequestException
from contextlib import closing
from bs4 import BeautifulSoup
import sqlite3
from time import sleep

def simple_get(url):
    """
    Attempts to get the content at `url` by making an HTTP GET request.
    If the content-type of response is some kind of HTML/XML, return the
    text content, otherwise return None.
    """
    try:
        with closing(get(url, stream=True)) as resp:
            if is_good_response(resp):
                return resp.content
            else:
                return None

    except RequestException as e:
        log_error('Error during requests to {0} : {1}'.format(url, str(e)))
        return None


def is_good_response(resp):
    """
    Returns True if the response seems to be HTML, False otherwise.
    """
    content_type = resp.headers['Content-Type'].lower()
    return (resp.status_code == 200
            and content_type is not None
            and content_type.find('html') > -1)


def log_error(e):
    """
    It is always a good idea to log errors.
    This function just prints them, but you can
    make it do anything.
    """
    print(e)


def get_all_word_by_letter(letter):
    words = []
    page_index = 0
    while True:
        print(f"processing {page_index}")
        raw_html = simple_get(f"https://idegen-szavak.hu/szavak/betu_szerint/{letter}/{page_index}")
        if len(raw_html) == 0:
            break
        html = BeautifulSoup(raw_html, 'html.parser')
        for item in html.select('.item'):
            # print(f"{i} : {item.h1.text}")
            # print(f"{item.p.text} \n")
            words.append(f"Word : {item.h1.text} \n Description: {item.p.text}")
        sleep(1)
        page_index += 5
    return words


def main():
    words = get_all_word_by_letter("a")
    for word in words:
        print(word)


if __name__ == '__main__':
    conn = sqlite3.connect('words.db')
    main()
