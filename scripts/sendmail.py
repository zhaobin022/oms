#!/usr/bin/python
# -*- coding: utf-8 -*-
import smtplib
import string
import sys
import getopt


def usage():
    print """sendmail is a send mail Plugins
    Usage:

    sendmail [-h|--help][-t|--to][-s|--subject][-m|--message]

    Options:
           --help|-h)
                  print sendmail help.
           --to|-t)
                  Sets sendmail to email.
           --subject|-s)
                   Sets the mail subject.
           --message|-m)
                   Sets the mail body
     Example:
            only one to email  user
           ./sendmail -t 'eric@nginxs.com' -s 'hello eric' -m 'hello eric,this is sendmail test!
            many to email  user
           ./sendmail -t 'eric@nginxs.com,yangzi@nginxs.com,zhangsan@nginxs.com' -s 'hello eric' -m 'hello eric,this is sendmail test!"""
    sys.exit(3)

try:
    options,args = getopt.getopt(sys.argv[1:],"ht:s:m:",["help","to=","subject=","message="])
except getopt.GetoptError:
    usage()
for name,value in options:
    if name in ("-h","--help"):
       usage()
    if name in ("-t","--to"):
# accept message user
       TO = value
       TO = TO.split(",")
    if name in ("-s","--title"):
       SUBJECT = value
    if name in ("-m","--message"):
       MESSAGE = value
       MESSAGE = MESSAGE.split('\\n')
       MESSAGE = '\n'.join(MESSAGE)

#smtp HOST
HOST = "smtp.163.com"
#smtp port
PORT = 25
#FROM mail user
USER = 'tjrenrenche2@163.com'
#FROM mail password
PASSWD = 'tjrenrenche2016'
#FROM EMAIL
FROM = "tjrenrenche2@163.com"

try:
    BODY = string.join((
       "From: %s" % FROM,
       "To: %s" % TO,
       "Subject: %s" % SUBJECT,
       "",
       MESSAGE),"\r\n")

    #smtp = smtplib.SMTP()
    print 1
    smtp = smtplib.SMTP(timeout=10)
    print 2
    smtp.set_debuglevel(1)
    print 3
    smtp.connect(HOST)
    print 4
    smtp.login(USER,PASSWD)
    print 6
    smtp.sendmail(FROM,TO,BODY)
    smtp.quit()
except Exception as e:
    print 'Exception: ', e
    print "UNKNOWN ERROR"
    print "please look help"
    print "./sendmail -h"
