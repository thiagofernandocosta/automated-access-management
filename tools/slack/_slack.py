import os
import requests
import json
import sys

slack_token = os.environ.get('SLACK_TOKEN')
email = os.environ.get('EMAIL')

def delete_slack_user(user_id):
    payload = {'token': slack_token, 'user': user_id}
    response = requests.delete(
        'https://slack.com/api/users.admin.setInactive', params=payload)
    print(response.content)

def invite_slack_user(email):
    payload = {'token': slack_token, 'email': email, 'resend': true}
    response = requests.get(
        'https://slack.com/api/users.admin.invite', params=payload)
    print(response.content)

if __name__ == "__main__":
    arg = sys.argv[1]
    if arg == 'apply':
        invite_slack_user(email)
    elif arg == 'destroy':
        user_id = email.split("@")[0]
        delete_slack_user(user_id)
