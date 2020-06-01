import os
import boto3
import sys
import logging

logging.basicConfig(level=logging.DEBUG)

def verify_ses():
    logging.debug('Send email to verify on SES')
    # is still in the sandbox, this address must be verified.
    recipient = os.environ.get('EMAIL')
    # AWS Region you're using for Amazon SES.
    aws_region = os.environ.get('AWS_REGION')
    # Create a new SES resource and specify a region.
    client = boto3.client('ses',region_name=aws_region)
    
    try:
        response = client.verify_email_address(
            EmailAddress=recipient,)   

    # Display an error if something goes wrong.
    except ClientError as e:
        logging.debug(e.response['Error']['Message'])
    else:
        logging.debug('Email has been sent successfully: {}'.format(response)) 

if __name__ == "__main__":
    arg = sys.argv[1]
    if arg == 'apply':
        verify_ses()
    elif arg == 'destroy':
        logging.debug('SES email: {} keeps verified'.format(arg))