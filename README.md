# wikinews

A quick Python script to send an email with the contents of Wikipedia's daily current events page.

## Setup

Create an email address to send from, then use an email sending service that allows sending over SMTP.
* Gmail recently (deprecated this support)[https://support.google.com/accounts/answer/6010255?rfn=1651196585577]).
* SendGrid removed (free email sending)[https://www.twilio.com/en-us/changelog/sendgrid-free-plan].
* Currently using AWS SES, but it's a pain to set up. See the Terraform configuration for Curio (here)[https://github.com/skyline-apps/curio/blob/main/src/infra/aws/email_sender.tf]. Follow instructions there to get SMTP credentials.

First run `git update-index --assume-unchanged email_config.json` to avoid checking in configuration changes.

Edit the fields in `email_config.json` to have sender account credentials and a recipient list.

```json
{
    "sender_server": "email-smtp.us-west-2.amazonaws.com",
    "sender_email": "sender@email.com",
    "sender_user": "<AWS Access Key ID>",
    "sender_password": "<Generated from AWS Secret Access Key>",
    "recipients": ["first@recipient.com", "second@recipient.com"]
}
```

Next, set up the virtual environment and install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

Run the `send_email.py` script. You'll probably want to e.g. set up a cron job to run this daily :)

```
0 5 * * * /home/kim/wikinews/.venv/bin/python3 /home/kim/wikinews/send_email.py > /home/kim/email.log 2>&1
```

## Development

Run `mypy send_email.py` to run type checking.
