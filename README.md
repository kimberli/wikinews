# wikinews

A quick Python script to send an email with the contents of Wikipedia's daily current events page.

## Setup

Edit the fields in `email_config.json` to have sender account credentials and a recipient list.

```json
{
    "sender_email": "sender@email.com",
    "sender_password": "senderpassword",
    "recipients": ["first@recipient.com", "second@recipient.com"]
}
```

## Usage

Run the `send_email.py` script. You'll probably want to e.g. set up a cron job to run this daily :)

```
0 5 * * * python3 /home/kim/wikinews/send_email.py > /home/kim/email.log 2>&1
```
