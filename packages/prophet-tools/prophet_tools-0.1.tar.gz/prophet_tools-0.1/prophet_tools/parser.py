import sys
import os
current = os.path.dirname(os.path.realpath(__file__))
sys.path.append(current)
from tools.auto_import import import_or_install

import_or_install('requests')
import_or_install('lxml')

import os
import requests
from lxml import etree
from urllib.request import urlopen
import contextlib

def xpath(xml, xpath):
    xml(xpath)[0].text

def read_html(html_file):
    local = f'file:///{html_file}'
    with contextlib.closing(urlopen(local)) as response:
        htmlparser = etree.HTMLParser()
        tree = etree.parse(response, htmlparser)
    return tree.xpath

def create_response_page(txt):
    dir_path = os.path.dirname(os.path.realpath(__file__)).replace('\\', '/')
    temp_file = f'{dir_path}/response_page.html'
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(txt)
    return temp_file

def parse(url, parameters, create_response_page_file=False, read_html_file=False):
    response = requests.get(url, params=parameters)
    if response.status_code != 200:
        print('HTTP error', response.status_code)
        return 'error'
    
    if create_response_page_file is True:
        temp_file = create_response_page(response.text)
        if read_html_file is True:
            xpath_tree = read_html(temp_file)
    else:
        temp_file = None
        xpath_tree = None

    return {
        'txt': response.text,
        'html file': temp_file,
        'xpath tree': xpath_tree
    }

# if __name__ == '__main__':
#     pass