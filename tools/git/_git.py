import os
import json
import requests
import sys
import logging
from requests.auth import HTTPBasicAuth

logging.basicConfig(level=logging.DEBUG)

api_key = os.environ.get('GITLAB_PRIVATE_TOKEN')
server = os.environ.get('GITLAB_HOST_URL')
email = os.environ.get('EMAIL')
groups = ['474', '407']

def api_get_user(email_user):
    user_rest = "/api/v4/users"
    url = "{}{}".format(server, user_rest)
    headers = { "PRIVATE-TOKEN": api_key }
    query = { 'search': email_user }                
    response = requests.request("GET", url, params=query, headers=headers)

    output = json.loads(response.text)
    logging.debug(json.dumps(output, sort_keys=True, indent=4, separators=(",", ": ")))
    return output

# levels availables
# gitlab.GUEST_ACCESS       = 10
# gitlab.REPORTER_ACCESS    = 20
# gitlab.DEVELOPER_ACCESS   = 30
# gitlab.MAINTAINER_ACCESS  = 40
# gitlab.OWNER_ACCESS       = 50
def api_add_user_to_group(user_id,group_id):
    user_rest = "/api/v4/groups/{}/members".format(group_id)
    url = "{}{}".format(server, user_rest)
    headers = { "PRIVATE-TOKEN": api_key }
    payload = "user_id={}&access_level={}".format(user_id, '30')
    response = requests.request( "POST", url, data=payload, headers=headers)

    logging.debug(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

def api_delete_user_from_group(user_id,group_id):
    user_rest = "/api/v4/groups/{}/members/{}".format(group_id, user_id)
    url = "{}{}".format(server, user_rest)
    headers = { "PRIVATE-TOKEN": api_key }
    requests.request("DELETE", url, headers=headers)

def delete_user_from_group():
    logging.debug('Deleting user {} from groups'.format(email)) 
    try:
        usr = api_get_user(email)
        if len(usr):
            account = usr[0]
            for group in groups:
                api_delete_user_from_group(account['id'],group)
    except Exception as exc:
        logging.debug(exc)

def add_user_to_group():
    logging.debug('Adding user {} to groups'.format(email)) 
    try:
        usr = api_get_user(email)
        if len(usr):
            account = usr[0]
            for group in groups:
                api_add_user_to_group(account['id'],group)
    except Exception as exc:
        logging.debug(exc)

if __name__ == "__main__":
    arg = sys.argv[1]
    if arg == 'apply':
        add_user_to_group()
    elif arg == 'destroy':
        delete_user_from_group()