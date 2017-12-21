#!/usr/bin/python
###################################Begin code from Stackoverflow =]]]]######################
import os
import smtplib
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import httplib2
from apiclient import discovery
import oauth2client
from oauth2client import client
from oauth2client import tools



try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

SCOPES = 'https://mail.google.com/'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~/freepbx_auto_recover')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-quickstart.json')

    store = oauth2client.file.Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatability with Python 2.6
            credentials = tools.run(flow, store)
        print 'Storing credentials to ' + credential_path
    return credentials

import base64
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import mimetypes
from httplib2 import Http
from apiclient import errors
from apiclient.discovery import build




def getService():
    credentials = get_credentials()
    service = build('gmail', 'v1', http=credentials.authorize(Http()))
    return service

def create_email_message(sender, to, subject, content):
    msg=MIMEText(content)
    msg['subject'] = subject
    msg['from'] = sender
    msg['to'] = to
    return {'raw': base64.urlsafe_b64encode(msg.as_string())}

def send_email_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print 'Message Id: %s' % message['id']
        return message
    except errors.HttpError, error:
        print 'An error occurred: %s' % error
##########################End of codes from Stackoverflow =]]]]#############################

import time
import smtplib
import mimetypes
from email.mime.multipart import MIMEMultipart
from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

def create_email_message_att(sender, to, subject, content, files_list):
    """Create email message with attachments."""
    msg = MIMEMultipart()
    msg['subject'] = subject
    msg.preamble = subject
    msg['from'] = sender
    msg['to'] = to
    msg.attach(MIMEText(content))

    for filetosend in files_list:
        ctype, encoding = mimetypes.guess_type(filetosend)
        if ctype is None or encoding is not None:
            ctype = "application/octet-stream"

        maintype, subtype = ctype.split("/", 1)

        if maintype == "text":
            fopen = open(filetosend)
            # Note: we should handle calculating the charset
            attachment = MIMEText(fopen.read(), _subtype=subtype)
            fopen.close()
        elif maintype == "image":
            fopen = open(filetosend, "rb")
            attachment = MIMEImage(fopen.read(), _subtype=subtype)
            fopen.close()
        elif maintype == "audio":
            fopen = open(filetosend, "rb")
            attachment = MIMEAudio(fopen.read(), _subtype=subtype)
            fopen.close()
        else:
            fopen = open(filetosend, "rb")
            attachment = MIMEBase(maintype, subtype)
            attachment.set_payload(fopen.read())
            fopen.close()
            encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=filetosend)
        msg.attach(attachment)

    return {'raw': base64.urlsafe_b64encode(msg.as_string())}

def email_send_it_monitor_down(log_buffer):
    """Send email to IT to alert XEN Server status."""
    emailSubject = 'Asterisk service is DOWN '+time.strftime("%d/%m/%Y")+' '+time.strftime("%H:%M:%S")
    receiver = ['tai.vd@mobivi.vn','an.hb@mobivi.vn','thi.db@mobivi.vn','huy.dc@mobivi.vn','vuong.nq@mobivi.vn']
    #receiver = ['an.hb@mobivi.vn']
    result_id = ''
    for emailaddr in receiver:
        emailMessage = create_email_message('it.bot@mobivi.vn', emailaddr, emailSubject, log_buffer)
        service = getService()
        emailSend = send_email_message(service, 'it.bot@mobivi.vn', emailMessage)
        result_id = result_id+(str(emailSend))+'\n'
    return result_id

def email_send_it_monitor_waning(log_buffer):
    """Send email to IT to alert XEN Server status."""
    emailSubject = 'Asterisk service status is WARNING '+time.strftime("%d/%m/%Y")+' '+time.strftime("%H:%M:%S")
    receiver = ['tai.vd@mobivi.vn','an.hb@mobivi.vn','thi.db@mobivi.vn','huy.dc@mobivi.vn','vuong.nq@mobivi.vn']
    #receiver = ['an.hb@mobivi.vn']
    result_id = ''
    for emailaddr in receiver:
        emailMessage = create_email_message('it.bot@mobivi.vn', emailaddr, emailSubject, log_buffer)
        service = getService()
        emailSend = send_email_message(service, 'it.bot@mobivi.vn', emailMessage)
        result_id = result_id+(str(emailSend))+'\n'
    return result_id

