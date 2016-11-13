"""A script to download slack archives."""

from os.path import abspath, dirname, join

from splinter import Browser
from splinter.exceptions import ElementDoesNotExist
import yaml

HERE = dirname(abspath(__file__))
CONFIG_PATH = join(HERE, '..', 'parktain', 'config.yaml')
with open(CONFIG_PATH, 'r') as ymlfile:
    slack = yaml.load(ymlfile).get('slack')


def wait_for_download_completion(browser):
    browser.visit("chrome://downloads/")
    # FIXME: Figure out what element needs to diappear/appear
    import time
    time.sleep(30)


with Browser('chrome') as browser:
    # Visit URL
    url = 'https://my.slack.com/services/export'
    browser.visit(url)
    browser.fill('domain', slack['domain'])
    browser.click_link_by_id('submit_team_domain')
    browser.fill('email', slack['email'])
    browser.fill('password', slack['password'])
    browser.click_link_by_id('signin_btn')
    try:
        button = browser.find_by_text('Start Export')[0]
        button.click()
    except ElementDoesNotExist:
        pass

    try:
        link = browser.find_link_by_partial_text('Ready for download')[0]
        link.click()
        wait_for_download_completion(browser)
    except ElementDoesNotExist:
        print('Could not download export file')
