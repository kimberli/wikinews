#/usr/bin/python
import datetime
import json
import logging
import os
import smtplib
import ssl
from typing import List

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr

import bs4
import requests

logging.basicConfig(level=logging.INFO)

DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'email_config.json')
_INTERNAL_WIKI_LINK = '/wiki'
_EXTERNAL_WIKI_LINK = 'https://en.wikipedia.org/wiki'
LINK_COLOR = '#888'


class Config:
    def __init__(self, config_filepath: str) -> None:
        with open(config_filepath, 'r') as config_file:
            config = json.load(config_file)
        self.server: str = config['sender_server']
        self.user: str = config['sender_user']
        self.password: str = config['sender_password']
        self.email: str = config['sender_email']
        self.recipients: List[str] = config['recipients']

def read_config(config_path = DEFAULT_CONFIG_PATH) -> Config:
    return Config(config_path)

def get_date() -> datetime.datetime:
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    return yesterday

def fetch_wikipedia_news(date):
    date_str = date.strftime('%Y_%B_%-d')
    logging.info('Fetching news from %s', date_str)

    response = requests.get('https://en.wikipedia.org/wiki/Portal:Current_events/' + date_str)

    page = bs4.BeautifulSoup(response.text, 'html.parser')
    content = page.findAll('div', { 'class': 'description' })[0]
    if not content:
        logging.error('Error fetching content')

    # Style all links.
    for link in content.findAll('a'):
        link['style'] = f'color: {LINK_COLOR}; text-decoration: none;'
        # Replace all internal /wiki links with links that work from email client.
        if link.has_attr('href') and link['href'].startswith(_INTERNAL_WIKI_LINK):
            link['href'] = _EXTERNAL_WIKI_LINK + link['href'][len(_INTERNAL_WIKI_LINK):]

    # Wrap the returned content with some styling.
    wrapper = page.new_tag('div', **{'style': 'max-width: 700px;'})
    content.wrap(wrapper)

    return wrapper

def send_email(config, date, content) -> None:
    subject = 'Current events - {}'.format(date.strftime('%B %d, %Y'))
    logging.info('Sending email: %s', subject)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = formataddr(("Wikinews", config.email))
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
    try:
        send_email(config, date, content)
    except:
        logging.exception("Failed to send email")
