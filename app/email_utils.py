import requests
import threading
from env import API_KEY, DOMAIN


def send_campaign_email(campaign):

    api_key = API_KEY
    domain = DOMAIN

    # Mailgun API URL for sending messages
    mailgun_url = f'https://api.mailgun.net/v3/{domain}/messages'

    # Email data
    data = {
        'from': campaign.sender_mail,
        'to': 'sirius.sonu2405@gmail.com',
        'subject': campaign.subject,
        'text': campaign.plain_text_content,
        'html': campaign.html_content,
    }

    # Send the email using the requests library
    response = requests.post(mailgun_url, auth=('api', api_key), data=data)

    # Check the response
    if response.status_code == 200:
        print(f"Email sent successfully to {data['to']}")
        return True
    else:
        print(f"Failed to send email: {response.text}")
        return False




def send_campaigns_in_parallel(campaigns):
    threads = []
    for campaign in campaigns:
        t = threading.Thread(target=send_campaign_email, args=(campaign,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()
