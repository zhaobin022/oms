from cmdb import models
import string
from random import choice
from utils.threadpool import thread_pool
from utils.cmdb_utils import operation_log
import paramiko
import pexpect
import re
import django.utils.timezone
import logging
logger = logging.getLogger('web_apps')

class UpdateServerPassword(object):
    def __init__(self,action_type,server_id_list,req):
        self.action_type = action_type
        self.server_id_list = server_id_list
        self.req = req

    def GenPassword(self,length=32,chars=string.ascii_letters+string.digits):
        return ''.join([choice(chars) for i in range(length)])




    def gen_password(self):
        cmdb_server_list = models.Server.objects.all()
        for s in cmdb_server_list:
            newpassword = self.GenPassword()
            s.new_pwd = newpassword
            s.save()


    def execute_cmd(self,s,args):
        try:
            cmd = args[0]
            logger.info('server %s execute cmd %s' % (s.ipaddress,cmd))
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(s.ipaddress,s.ssh_port,'root', s.root_pwd,timeout=5)
            stdin, stdout, stderr = ssh.exec_command(cmd)
            result = stdout.readlines()
            ssh.close()
        except Exception , e:
            logger.info(str(e))
            result = ['1',str(e)]
        logger.info(result)
        if int(result[0]) == 0:
            s.ssh_check=0
        else:
            s.ssh_check=1
        s.save()

    def ssh_check(self):
        server_list = models.Server.objects.filter(id__in=self.server_id_list)
        thread_pool(server_list,'echo 0',fun=self.execute_cmd)

    def ret_pass_tag(self):
        cmdb_server_list = models.Server.objects.all()
        for s in cmdb_server_list:
            s.change_password_tag = 1
            s.save()


    def ssh_cmd(self,s,args):
        log_info = "old pwd : %s      new pwd : %s" % (s.root_pwd,s.new_pwd)
        operation_log(3,self.req.user,s,log_info)
        timeout = 10
        ret = -1
        logger.info('ssh -p%s %s@%s' % (s.ssh_port,'root',s.ipaddress))
        ssh = pexpect.spawn('ssh -p%s %s@%s' % (s.ssh_port,'root',s.ipaddress))
        try:
            i = ssh.expect(['password:', 'continue connecting (yes/no)?'], timeout=timeout)
            if i == 0 :
                ssh.sendline(s.root_pwd)
            elif i == 1:
                ssh.sendline('yes\n')
                ssh.expect('password: ',timeout=timeout)
                ssh.sendline(s.root_pwd)
            ssh.sendline('passwd')

     #       r = ssh.read()
            ssh.expect('New password:',timeout=timeout)
            ssh.sendline(s.new_pwd)
            ssh.expect('Retype new password:',timeout=timeout)
            ssh.sendline(s.new_pwd)
            ssh.expect('#',timeout=timeout)
            ssh.sendline('exit')

            pattern = re.compile(r'.*tokens updated successfully.*',re.S)
            result = ssh.before
            logger.info(result)
            if pattern.match(result).group():
                ret = 0
            else:
                ret = 1
        except pexpect.EOF:
            ssh.close()
            ret = 1
            logger.info('in eof')
        except pexpect.TIMEOUT:
            ssh.close()
            ret = 1
            logger.info('timeout')
        except Exception,e:
            logger.info(str(e))
            ret = 1
        if ret == 0:
            s.change_password_tag = 0
            logger.info("old password : " + s.root_pwd)
            s.root_pwd = s.new_pwd
            s.update_password_time = django.utils.timezone.now()
            s.save()
        elif ret == 1:
            s.change_password_tag = 1
        s.save()
        # return ret

    def update_password(self):
        server_list = models.Server.objects.filter(id__in=self.server_id_list)
        thread_pool(server_list,fun=self.ssh_cmd)

    def handler(self):
        if hasattr(self,self.action_type):
            f = getattr(self,self.action_type)
            f()
            return {'status':'finish'}
        else:
            return {'status':'finish'}
