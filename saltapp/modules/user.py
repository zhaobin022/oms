__author__ = 'zhaobin022'

from saltapp.modules.base_module import BaseStateModule

class User(BaseStateModule):
    def uid(self,*args,**kwargs):
        self.cmd += "-u %s "  % args[0]

    def gid(self,*args,**kwargs):
        self.cmd += "-g %s "  % args[0]
    def home(self,*args,**kwargs):
        self.cmd += "-d %s "  % args[0]
    def shell(self,*args,**kwargs):
        self.cmd += "-s %s "  % args[0]


    def parse_require(self,*args,**kwargs):
        username = args[0]
        require = "grep -wq %s  /etc/passwd" % username
        return require
    def present(self,*args,**kwargs):

        self.cmd = "useradd "+self.cmd+" "+args[0]
        self.d['cmd_list'].append( self.cmd)
