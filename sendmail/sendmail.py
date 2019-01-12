'''
The module is to send mail.
it will read config file first, then read arguments from args.the latter value will override same parameter set in config file
you must sepecify mail body and mail subject in args
'''
import sys
import os
import smtplib
import argparse
import json
from inspect import stack
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


DEFAULT_MAIL_FROM = "FIH-BDC-Report@fih-foxconn.com"
DEFAULT_MAIL_TO = "Baochun.Dai; ongmei.liu; Queenie.KW.Kun"
DEFAULT_MAIL_DOMAIN_NAME = "fih-foxconn.com"
STANDARD_SMTP_OVER_SSL_PORT = 465
STANDARD_SMTP_PORT = 25
DEFAULT_MAIL_CONFIG_JSON = "mail.json"
DEFAULT_ENCODING_UTF8 = "utf-8"

# Flag to output verbose information or not
verbose_flag = False


def str2bool(v):
    ''' convert yes, true, t, y 1 to boolean True and convert no,false,f,n,0 to boolean False '''
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

def d(msg):
    if verbose_flag:
        # print("V: %d %d %s" % (stack()[1].lineno, stack()[2].lineno, msg))
        print("V: %s" % msg)
        sys.stdout.flush()

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--mail_to", required=False, nargs='+', help='recipient list in to_line')
    parser.add_argument("-f", "--mail_from", required=False, help='who to send the mail')
    parser.add_argument('-s', "--subject", required=False, help='mail subject')
    parser.add_argument("-c", "--cc", nargs='+', help='recipient list in cc line')
    parser.add_argument('-b', "--body", help='mail message/body,will be encoded to HTML format')
    parser.add_argument('-a', "--attachments", nargs='+', help='attachments')
    #parser.add_argument('-H', "--html_content", help='html body')
    parser.add_argument('-C', "--config_file", default=DEFAULT_MAIL_CONFIG_JSON, help='config_file for all information except mail message')
    parser.add_argument('-S', "--smtp_server", help='smtp server name or address')
    parser.add_argument('-P', "--port", help='smtp server port')
    parser.add_argument('-u', "--user", help='user to login smtp server')
    parser.add_argument('-p', "--password", help='password to login smtp server')
    parser.add_argument('-l', "--ssl", action='store_true',  default=False,  help='enable ssl when login stmp server, default: False')
    parser.add_argument('-v', "--verbose", action='store_true',  default=False,  help='output verbose information if specified')
    parser.add_argument('-e', "--encoding", default=DEFAULT_ENCODING_UTF8,  help='message encoding, default:utf-8')

    return parser.parse_args()


class MailClent:
    def __init__(self, host=None, user=None, password=None, enable_ssl=False, port=STANDARD_SMTP_PORT):

        ### init smtp server info
        self.host = host
        self.user = user
        self.password = password
        self.enable_ssl = enable_ssl
        self.port = port
        #self.set_conn_info(host, user, password,enable_ssl, port, override=True)

        # init mail info
        self.msg = None
        self.mail_config_json = None
        self.mail_to = None
        self.mail_from = None
        self.subject = None
        self.body = None # mail body from arguments
        self.cc = None
        self.attachements = None
        self.encoding = DEFAULT_ENCODING_UTF8
        # self.subject_prefix = None

    def set_conn_info(self, host=None, user=None, password=None, enable_ssl=False, port=None, override=False):
        '''
        set smtp server connection related info: host, user,password, port, enable ssl or not.
        parameter override indicates that if the parameter was assigned , if use new value to override or not.
       '''
        if host and ((not self.host) or override): # if force override or member value was not assigned
            self.host = host
        if user and ((not self.user) or override):
            self.user = user
        if password and ((not self.password) or override):
            self.password = password
        if (enable_ssl is not None) and ((self.enable_ssl is None) or override):
            self.enable_ssl = enable_ssl
        if port and ((not self.port) or override):
            self.port = port


    def set_mail_info(self, mail_from, mail_to, cc=None, subject=None, body=None, attachements=None, encoding=DEFAULT_ENCODING_UTF8, override=False):
        '''
        set mail sender, to list, cc list, subject, body, attachements, encoding
        parameter override indicates that if the parameter was assigned , use new value to override  or not.
        '''
        if mail_from and ((not self.mail_from) or override):
            from_list = self.append_email_address_with_domain_name([mail_from])
            self.mail_from = from_list[0]
        if mail_to and ((not self.mail_to) or override):
            to_list = self.append_email_address_with_domain_name(mail_to)
            d("set mail TO list: %s" % to_list)
            self.mail_to = to_list
        if cc and ((not self.cc) or override):
            cc_list = self.append_email_address_with_domain_name(cc)
            d("set mail CC list: %s" % cc_list)
            self.cc = cc_list
        if subject and ((not self.subject) or override):
            self.subject = subject
        if body and ((not self.body) or override):
            self.body = body
        if attachements and ((not self.attachements) or override):
            self.attachements = attachements
        if self.encoding and ((not self.encoding) or override):
            self.encoding = encoding

    def set_encoding(self, encoding=DEFAULT_ENCODING_UTF8):
        ''' set encoding '''
        if encoding:
            self.encoding = encoding

    def read_config(self, config_file):
        '''
        read smtp and part of mail related information from config file of json format
        if the member value was specified,it won't be overridden by config file settings
        '''
        self.config_file = config_file
        if self.config_file:
            d("config_file is : %s" % self.config_file)
            try:
                with open(self.config_file, 'r') as f:
                    self.mail_config_json = json.load(f)
                    d("mail_config_json: %s" % self.mail_config_json)
                    # read smtp connection related information
                    self.set_conn_info(self.mail_config_json['host'],
                        self.mail_config_json['user'],
                        self.mail_config_json['password'],
                        self.mail_config_json['enable_ssl'],
                        self.mail_config_json['port'],
                        override=False)

                    self.set_mail_info(self.mail_config_json['mail_from'],
                        self.mail_config_json['mail_to'],
                        self.mail_config_json['cc'])

            except IOError as e:
                print("Failed to open \"%s\", e=%s" % (self.config_file, e))
            except Exception as e:
                print("Failed to load \"%s\", e=%s" % (self.mail_config_json, e))
        else:
            d("config_file is empty")

    def construct_attachment_list(self, attachements):
        ''' construct attachment list of MIMEText by file path '''
        attachement_list = []
        if attachements and len(attachements) > 0:
            for item in attachements:
                mime_attachement = MIMEText(open(item, 'rb').read(), 'base64', self.encoding)
                mime_attachement["Content-Type"] = 'application/octet-stream'
                (file_path, file_name) = os.path.split(item)
                mime_attachement["Content-Disposition"] = 'attachment; filename="%s"' % file_name
                attachement_list.append(mime_attachement)
        return attachement_list

    def construct_msg(self):
        '''
        construct msg for mail, the body is of HTML format
        '''
        self.msg = MIMEMultipart()
        self.msg['Subject'] = self.subject
        self.msg['From'] = self.mail_from
        self.msg['To'] = ";".join(self.mail_to)
        if not self.body:
            self.body = ' '
        # handle with mail body of html format
        mime_body = MIMEText(self.body,_subtype="html",_charset=DEFAULT_ENCODING_UTF8)
        self.msg.attach(mime_body)
        # handle with attachments
        attachement_list = self.construct_attachment_list(self.attachements)
        for attachment in attachement_list:
            self.msg.attach(attachment)

    def append_email_address_with_domain_name(self, email_address_list):
        '''
        if email address only contains email account without @yyy.zzz,then
        append with default domain name.
        '''
        new_email_address_list = []
        if email_address_list:
            for email_address in email_address_list:
                email_address = email_address.strip()
                if email_address.find('@') == -1:
                    email_address += '@' + DEFAULT_MAIL_DOMAIN_NAME
                new_email_address_list.append(email_address)
        return new_email_address_list

    def conn(self):
        '''
        To establis the connection to the smtp server
        if host is not specified, then use localhost
        '''
        if not self.host:
            d("host is None, set it to localhost")
            self.host = "localhost"
        d("smtp server: %s" % self.host)

        # create smtp instance according to ssl is enabled or not
        if self.enable_ssl:
            if not self.port:
                self.port = STANDARD_SMTP_OVER_SSL_PORT  # 465
            self.smtp = smtplib.SMTP_SSL(self.host, self.port)
        else:
            if not self.port:
                self.port = STANDARD_SMTP_PORT  # 25
            self.smtp = smtplib.SMTP(self.host, self.port)

        # output smtp debug messages for connection
        # and for all messages sent to and received from the server
        # For python 3.5 or higher only:
        # a value of 2 for level results in these messages being timestamped.
        if verbose_flag:
            self.smtp.set_debuglevel(2)

        # login with user and password if they are not empty
        if self.user and self.password:
            self.smtp.login(self.user, self.password)

    def send_mail(self,mail_from=None, mail_to=None, cc=None, subject=None, message=None, attachements=None, encoding=DEFAULT_ENCODING_UTF8):
        '''
        to send mail. if the parameters are not None,<br>
        it will override the same parameter value read from config file
        '''
        self.set_mail_info(mail_from, mail_to, cc, subject, message, attachements, encoding, True)
        self.conn()
        self.construct_msg()
        self.smtp.sendmail(self.mail_from, self.mail_to, self.msg.as_string())


def get_mail_info_from_args(args):
    '''
    Retrive the arguments from args to avoid exception if read non-existed arugment 
    '''
    host = None
    user = None
    password = None
    enable_ssl = False
    port = None
    mail_from = None
    mail_to = None
    cc = None
    subject = None
    body = None
    attachments = None
    encoding = DEFAULT_ENCODING_UTF8

    if args.smtp_server:
        host = args.smtp_server
    if args.user:
        user = args.user
    if args.password:
        password = args.password
    if args.ssl is not None:
        enable_ssl = args.ssl
    if args.port:
        port = args.port
    if args.mail_from:
        mail_from = args.mail_from
    if args.mail_to:
        mail_to = args.mail_to
    if args.cc:
        cc = args.cc
    if args.subject:
        subject = args.subject
    if args.body:
        body = args.body
    if args.attachments:
        attachments = args.attachments
    if args.encoding:
        encoding = args.encoding
    # if args.html_content:
    #     body += args.html_content

    if host is None:
        host = "localhost"

    return host, user, password, enable_ssl, port, mail_from, mail_to, cc, subject, body,attachments,encoding

def _main():
    global verbose_flag
    args = parse_args()
    print(args)
    if args.verbose:
        verbose_flag = True
    host, user, password, enable_ssl, port, mail_from, mail_to, cc, subject, body, attachements,encoding = get_mail_info_from_args(args)

    mail_client = MailClent(host,user,password,enable_ssl,port)

    mail_client.read_config(args.config_file)
    # if arguments are not None, then they will override settings in config file
    mail_client.send_mail(mail_from, mail_to, cc, subject, body,attachements,encoding)

if __name__ == '__main__':
    _main()