"""Example app to login to imdbPRO"""
import argparse
import mechanicalsoup

#content_url = 'https://pro-labs.imdb.com/list?ref_=hm_nv_mt_myl'
content_url = 'https://pro-labs.imdb.com/company/co0144901/'
login_url = 'https://pro-labs.imdb.com/login'

USERNAME = 'liu_brandon@bah.com'
PASSWORD = 'brandon229271'

browser = mechanicalsoup.Browser()

login_page = browser.get(login_url)
soup = login_page.soup

login_form = soup.select("#content_box")[0].select("form")[0]

# specify username and password
login_form.select("#email")[0]['value'] = USERNAME
login_form.select("#password")[0]['value'] = PASSWORD

page2 = browser.submit(login_form, login_page.url)

content_page = browser.get(content_url)

def scrapeURL(url):


print(content_page.soup.encode('utf-8'))
