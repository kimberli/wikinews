#/usr/bin/python
import datetime
import json
import os
import smtplib
import ssl

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import bs4
import requests


DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'email_config.json')

def read_config(config_path = DEFAULT_CONFIG_PATH):
    with open(config_path, 'r') as config_file:
        config = json.load(config_file)
    return config['sender_email'], config['sender_password'], config['recipients']

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
    return content

def send_email(sender_email, sender_password, recipients, date, content):
    subject = 'Current events - {}'.format(date.strftime('%B %d, %Y'))
    print('Sending email:', subject)
    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = ','.join(recipients)

    text = 'TODO'
    html = content

    part1 = MIMEText(text, "plain")
    part2 = MIMEText(html, "html")

    msg.attach(part1)
    msg.attach(part2)

    port = 465  # For SSL

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipients, msg.as_string())

if __name__ == "__main__":
    sender_email, sender_password, recipients = read_config()
    date = get_date()
    content = fetch_wikipedia_news(date)
    send_email(sender_email, sender_password, recipients, date, content)
