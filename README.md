# wikinews

A quick Python script to send an email with the contents of Wikipedia's daily current events page.

## Setup

Create an email address to send from, then use an email sending service that allows sending over SMTP (since Gmail recently (deprecated this support)[https://support.google.com/accounts/answer/6010255?rfn=1651196585577]).
The service I use is Sendgrid via SMTP. 

Edit the fields in `email_config.json` to have sender account credentials and a recipient list.

```json
{
    "sender_server": "smtp.sendgrid.net",
    "sender_email": "sender@email.com",
    "sender_user": "apikey",
    "sender_password": "<API key from Sendgrid>",
    "recipients": ["first@recipient.com", "second@recipient.com"]
}
```

## Usage

Run the `send_email.py` script. You'll probably want to e.g. set up a cron job to run this daily :)

```
0 5 * * * python3 /home/kim/wikinews/send_email.py > /home/kim/email.log 2>&1
```

## Development

Run `mypy send_email.py` to run type checking.
