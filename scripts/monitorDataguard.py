#!/usr/bin/python
# -*- coding: utf-8 -*-


#import cx_Oracle
import string
from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
import sys
import getopt
import re


#        command_line    $USER1$/monitorDataguard.py -H $HOSTADDRESS$ -t $ARG1$ -u $ARG2$ -p $ARG3$ -s $ARG4$

def usage():
    print '''Usage : monitorDataguard.py -H ip -t [cluster/single] -u user -p pasword -s sid '''
try:
    opts, args = getopt.getopt(sys.argv[1:], 'H:t:u:p:s:')
except getopt.GetoptError:
    usage()
    sys.exit()

# p = re.compile(r"^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))$")
# ip = opts[0][1]
# flag = p.match(ip)
# if not flag:
#     sys.exit()

opts_dic = dict(opts)

host = opts_dic['-H']
instance_type = opts_dic['-t']
user = opts_dic['-u']
pwd = opts_dic['-p']
sid = opts_dic['-s']



conn = cx_Oracle.connect('%s/%s@%s/%s' % (user,pwd,host,sid))
cursor = conn.cursor ()


# detect cluster sql
cursor.execute (''' select max(sequence#) from v$archived_log where dest_id=2 and thread#=%s ''' % '1')
#rows = cursor.fetchall()
rows = cursor.fetchone()
thread1Primary = rows[0]
cursor.execute (''' select max(sequence#) from  v$log_history  where thread#=%s ''' % '1')
rows = cursor.fetchone()
thread1Standby = rows[0]

cursor.execute (''' select max(sequence#) from v$archived_log where dest_id=2 and thread#=%s ''' % '2')
rows = cursor.fetchone()
thread2Primary = rows[0]
cursor.execute (''' select max(sequence#) from  v$log_history  where thread#=%s ''' % '2')
rows = cursor.fetchone()
thread2Standby = rows[0]

cursor.close ()
conn.close ()

diffThread1 = thread1Primary - thread1Standby
diffThread2 = thread2Primary - thread2Standby

if instance_type == 'cluster':
    if diffThread1 != 0 or diffThread2 !=0:
        msg = u' DATAGUARD ERROR : thread1Primary = %s thread1Standby = %s thread2Primary = %s thread2Standby = %s ' % (str(thread1Primary),str(thread1Standby),str(thread2Primary),str(thread2Standby))
        sys.exit(2)
    else:
        msg = u' DATAGUARD OK : thread1Primary = %s thread1Standby = %s thread2Primary = %s thread2Standby = %s ' % (str(thread1Primary),str(thread1Standby),str(thread2Primary),str(thread2Standby))
        print msg

elif instance_type == 'single':
    if diffThread1 != 0:
        msg = u' DATAGUARD ERROR : thread1Primary = %s thread1Standby = %s ' % (str(thread1Primary),str(thread1Standby))
        sys.exit(2)
    else:
        msg = u' DATAGUARD OK : thread1Primary = %s thread1Standby = %s ' % (str(thread1Primary),str(thread1Standby))
        print msg#detect single instance

