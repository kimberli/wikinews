#/usr/bin/python
import datetime
import json
import os
import smtplib
import ssl
from typing import List

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import bs4
import requests


DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'email_config.json')
_INTERNAL_WIKI_LINK = '/wiki'
_EXTERNAL_WIKI_LINK = 'https://en.wikipedia.org/wiki'


class Config:
    def __init__(self, config_filepath: str):
        with open(config_filepath, 'r') as config_file:
            config = json.load(config_file)
        self.server: str = config['sender_server']
        self.user: str = config['sender_user']
        self.password: str = config['sender_password']
        self.email: str = config['sender_email']
        self.recipients: List[str] = config['recipients']

def read_config(config_path = DEFAULT_CONFIG_PATH) -> Config:
    return Config(config_path)

def get_date():
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    return yesterday

def fetch_wikipedia_news(date):
    date_str = date.strftime('%Y_%B_%-d')
    print('Fetching news from', date_str)

    response = requests.get('https://en.wikipedia.org/wiki/Portal:Current_events/' + date_str)

    page = bs4.BeautifulSoup(response.text, 'html.parser')
    content = page.findAll('div', { 'class': 'description' })[0]
    if not content:
        print('Error fetching content')

    # Replace all internal /wiki links with links that work from email client.
    for link in content.findAll('a'):
        if link.has_attr('href') and link['href'].startswith(_INTERNAL_WIKI_LINK):
            link['href'] = _EXTERNAL_WIKI_LINK + link['href'][len(_INTERNAL_WIKI_LINK):]

    return content

def send_email(config, date, content):
    subject = 'Current events - {}'.format(date.strftime('%B %d, %Y'))
    print('Sending email:', subject)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = config.email
    msg['To'] = ','.join(config.recipients)

    text = 'TODO'
    html = content

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    msg.attach(part1)
    msg.attach(part2)

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(config.server, port, context=context) as server:
        server.login(config.user, config.password)
        server.sendmail(config.email, config.recipients, msg.as_string())

if __name__ == "__main__":
    config = read_config()
    date = get_date()
    content = fetch_wikipedia_news(date)
    send_email(config, date, content)
