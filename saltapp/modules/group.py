__author__ = 'zhaobin022'
from saltapp.modules.state import BaseStateModule


class Group(BaseStateModule):

    def gid(self,*args,**kwargs):
        self.cmd += "-g %s "  % args[0]

    def parse_require(self,*args,**kwargs):
        group_name = args[0]
        require = "grep -wq %s  /etc/group" % group_name
        return require


    def present(self,*args,**kwargs):
        self.cmd = "groupadd "+self.cmd+" "+args[0]
        self.d['cmd_list'].append( self.cmd)
