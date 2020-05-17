# -*- coding: utf-8 -*-
import requests
from time import sleep
from urlparse import urlparse
from bs4 import BeautifulSoup
from selenium import webdriver
from tmall_crawler import constants as C
from tmall_crawler.helpers import sitemap_generator, remove_element, insert_js, replace_title

import os
import re
import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s  - %(message)s')


class Tmall(object):
    def __init__(self, url, path=None):
        self.url = url
        self.path = path
        self.urls = []
        self.finished_url = []
        # self._session = requests.Session()
        # self._session.headers.update(C.USER_AGENT)
        self._driver = webdriver.PhantomJS()

    def path_process(self, url_obj):
        dir, filename = os.path.split(url_obj.path)
        if self.path is not None:
            prefix_dir = os.path.join(self.path, dir.strip('/'))
        else:
            prefix_dir = os.path.join(url_obj.netloc, dir.strip('/'))

        if (dir == '/' or not dir) and not filename:
            filename = 'index.html'

        if not os.path.isdir(prefix_dir):
            os.makedirs(prefix_dir)

        logging.info('PREFIX DIR IS {}'.format(prefix_dir))
        logging.info('FILENAME IS {}'.format(filename))

        return prefix_dir, filename

    def move_to_element(self, el):
        footer_y = int(el.location['y'])
        for y in range(0, footer_y, 300):
            self._driver.execute_script('window.scrollTo(0, {})'.format(y))
            sleep(0.2)

    def get_content(self, url_obj):
        url = url_obj.geturl()
        self._driver.get(url)
        content = self._driver.page_source  # if 'widgetAsync' in content:
        return content

    def process_content(self, url_obj, bs_obj):
        remove_element(bs_obj)
        insert_js(bs_obj)

        for item in bs_obj.find_all('a', href=re.compile(r'.*//{}.*'.format(url_obj.netloc))):
            url_obj = urlparse(item.attrs['href'])
            item.attrs['href'] = url_obj.path
            _url = 'https://' + url_obj.netloc + url_obj.path
            if _url not in self.urls:
                self.urls.append(_url)

    def _get(self, url):
        url = url.strip('/')
        if url in self.finished_url:
            return

        url_obj = urlparse(url)

        content = self.get_content(url_obj)

        prefix_dir, filename = self.path_process(url_obj)

        if 'widgetAsync' in content:
            self.move_to_element(
                self._driver.find_element_by_id(C.FOOTER_ID))
            content = self._driver.page_source

        bs_obj = BeautifulSoup(content, 'lxml')
        '''selenium page source 解码有问题，借助 bs4 解码'''
        self.process_content(url_obj, bs_obj)

        if filename.startswith('index'):
            sites = requests.get(C.TASK_LIST).json()
            for site in sites:
                if url == site['url'].strip('/') and site['title'] is not None:
                    title = site['title']
                    replace_title(bs_obj, title)

        with open(os.path.join(prefix_dir, filename), 'wb') as f:
            f.write(str(bs_obj.prettify('utf-8')))
            logging.info('DOWNLOAD PAGE {} TO {}'.format(url, f.name))
            self.finished_url.append(url)

        # bs_obj = BeautifulSoup(res.text, 'lxml')
        for _url in self.urls:
            self._get(_url)

    def get(self):
        self._get(self.url)
        self.generate_sitemap(os.path.join(
            self.path or urlparse(self.url).netloc, 'sitemap.xml'))

    def generate_sitemap(self, path):
        with open(path, 'w') as f:
            f.write(sitemap_generator(self.finished_url))

    def close(self):
        self._driver.close()
