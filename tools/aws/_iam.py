import os
import boto3
import logging
import sys
import random
import string

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
logging.basicConfig(level=logging.DEBUG)

import mail
from mail import _template
from mail import _mail

user = os.environ.get('EMAIL')
absolute_path = path = os.path.dirname(os.path.abspath(__file__))
template_html = '/template/aws.html'

def random_pw(stringLength=10):
    """Generate a random string of letters, digits and special characters """
    password_characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(password_characters) for i in range(stringLength))

def get_aws_session():
    """Create session aws from environent variables """
    session = boto3.Session(aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
                            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY'),
                            region_name=os.environ.get('AWS_DEFAULT_REGION'))
    return session

def api_delete_user():
    session = get_aws_session()
    iam = session.client('iam')    
    try:
        logging.debug('Deleting user: {}'.format(user)) 
        iam.delete_login_profile(UserName=user)
        # Remove user from group
        iam.remove_user_from_group(GroupName='user-readonly',UserName=user)
        # Remove user
        iam.delete_user(UserName=user)
    
    # Display an error if something goes wrong.	
    except ClientError as e:
        logging.debug(e.response['Error']['Message']) 
    else:
        logging.debug('User deleted successfully!') 

def api_create_user():
    session = get_aws_session()
    iam = session.client('iam')

    try:
        logging.debug('Creating user: {}'.format(user))
        iam.create_user(UserName=user)
        # Generate random password
        password_generate = random_pw(20)
        iam.create_login_profile(
            UserName=user,
            Password=password_generate,
            PasswordResetRequired=True)
        # Adding to group
        iam.add_user_to_group(GroupName='user-readonly',UserName=user)

    # Display an error if something goes wrong.	
    except ClientError as e:
        logging.debug(e.response['Error']['Message'])
    else:
        logging.debug('User created successfully!') 
        return password_generate

def api_create_access_key():
    try:
        session = get_aws_session()
        iam = session.client('iam')
        response = iam.create_access_key(UserName=user)
        user_access_key = response['AccessKey']['AccessKeyId']
        user_secret_access_key = response['AccessKey']['SecretAccessKey']
        
    except ClientError as e:
        logging.debug(e.response['Error']['Message']) 
    else:
        logging.debug('Access Key created successfully!') 
        return user_access_key, user_secret_access_key

def api_delete_access_key():
    try:
        session = get_aws_session()
        iam = session.client('iam')
        meta_data = iam.list_access_keys(UserName=user)
        if meta_data:
            meta_user = meta_data['AccessKeyMetadata'][0]
            if meta_user:
                access_key_user = meta_user['AccessKeyId']
                # delete access_key_user found
                if access_key_user:
                    iam.delete_access_key(UserName=user, AccessKeyId=access_key_user)
    
    except ClientError as e:
        logging.debug(e.response['Error']['Message']) 
    else:
        logging.debug('Access key deleted successfully!') 

def create_user():
    logging.debug('Creating access user on aws...')
    # credentials
    user_mail = user
    user_password = api_create_user()
    (user_access_key,user_secret_access_key) = api_create_access_key()
    
    # dictionary to populate template
    thisdict = {"email_user": user_mail,
                "email_password": user_password,
                "access_key": user_access_key,
                "secret_key": user_secret_access_key
                }

    path_file = '{}/{}'.format(absolute_path, template_html)
    generate_template_html = _template.generate_body_from_template(thisdict, path_file)

    # send email with filled template
    _mail.send_mail(user_mail, generate_template_html)

def delete_user():
    logging.debug('Deleting access user on aws...')
    api_delete_access_key()
    api_delete_user()

if __name__ == "__main__":
    arg = sys.argv[1]
    if arg == 'apply':
        create_user()
    elif arg == 'destroy':
        delete_user()
    