__author__ = 'zhaobin022'
from saltapp.modules.base_module import BaseStateModule

class File(BaseStateModule):

    def source(self,*args,**kwargs):
        pass
    def user(self,*args,**kwargs):
        pass
    def group(self,*args,**kwargs):
        pass
    def mode(self,*args,**kwargs):
        pass

    def parse_require(self,*args,**kwargs):
        file_path = args[0]
        require = "test -f  %s" % file_path
        return require
    def managed(self,*args,**kwargs):
        self.file_dic = kwargs['sub_dic']
        self.file_dic.insert(0,{'minion_id':kwargs['minion_id']})
        print 'in managed................',self.file_dic