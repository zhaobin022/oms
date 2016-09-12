import paramiko
import logging
logger = logging.getLogger('web_apps')

def execute_cmd(s,cmd):
    try:

        logger.info('server %s execute cmd %s' % (s.ipaddr,cmd))
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(s.ipaddr,s.port,s.username, s.password)
        stdin, stdout, stderr = ssh.exec_command(cmd)
        result = stdout.readlines()
        ssh.close()
    except Exception , e:
        logger.info(str(e))
        return ['1',str(e)]
    return result