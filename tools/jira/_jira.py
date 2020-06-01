import os
import requests
import time
import sys
import logging

from requests.auth import HTTPBasicAuth
import json

logging.basicConfig(level=logging.DEBUG)

api_user    = os.environ.get('JIRA_EMAIL') 
api_key     = os.environ.get('JIRA_TOKEN')
server      = os.environ.get('JIRA_SERVER')
email       = os.environ.get('EMAIL')
groups      = ['android-workspace','ios-workspace','general-users']

def api_delete_user(account_id):
    user_rest       = "/rest/api/3/user"
    url             = "%s%s" % (server, user_rest)
    auth            = HTTPBasicAuth(api_user, api_key)
    query           = { 'accountId': account_id }                
    response        = requests.request("DELETE", url, params=query, auth=auth)

    logging.debug(response)

def api_get_user(email_user):
    user_rest       = "/rest/api/3/user/bulk/migration"
    url             = "%s%s" % (server, user_rest)
    auth            = HTTPBasicAuth(api_user, api_key)
    headers         = { "Accept": "application/json" }
    query           = { 'username': email_user }                
    response        = requests.request("GET", url, headers=headers, params=query, auth=auth)

    output = json.loads(response.text)
    logging.debug(json.dumps(output, sort_keys=True, indent=4, separators=(",", ": ")))
    return output

def api_add_user_to_group(account_id, group):
    group_user_rest = "/rest/api/3/group/user"
    url             = "%s%s" % (server, group_user_rest)
    auth            = HTTPBasicAuth(api_user, api_key)
    headers         = { "Accept": "application/json", "Content-Type": "application/json" }
    query           = { 'groupname': group }
    payload         = json.dumps({"accountId": account_id})
    response        = requests.request("POST", url, data=payload, headers=headers, params=query, auth=auth)
    
    logging.debug(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

def api_add_user(email_user):
    user_rest       = "/rest/api/3/user"
    url             = "%s%s" % (server, user_rest)
    auth            = HTTPBasicAuth(api_user, api_key)
    headers         = { "Accept": "application/json", "Content-Type": "application/json" }
    payload         = json.dumps({ "emailAddress": email_user, "displayName": email_user })
    response        = requests.request("POST", url, data=payload, headers=headers, auth=auth)
    # api takes a little time to persist
    time.sleep(10)
    logging.debug(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

def add_user_to_group():
    logging.debug('Adding user {} to jira groups'.format(email))
    username = email.split('@')[0]
    user = api_get_user(username)
    if len(user):
        account_id = user[0]['accountId']
        for group in groups:
            api_add_user_to_group(account_id,group)

def add_user():
    logging.debug('Adding user {} to jira'.format(email)) 
    api_add_user(email)

def delete_user():
    logging.debug('Deleting user {} from jira'.format(email)) 
    username = email.split('@')[0]
    user = api_get_user(username)
    if len(user):
        account_id = user[0]['accountId']
        api_delete_user(account_id)

if __name__ == "__main__":
    arg = sys.argv[1]
    if arg == 'apply':
        add_user()
        add_user_to_group()        
    elif arg == 'destroy':
        delete_user()