from saltapp.modules.base_module import BaseStateModule

class Pkg(BaseStateModule):
    def parse_require(self,*args,**kwargs):
        package_name = args[0]
        require = "dpkg --status %s &> /dev/null" % package_name
        return require


    def pkgs(self,*args,**kwargs):
        pass

    def installed(self,*args,**kwargs):
        pkgs = kwargs['sub_dic'][0]['pkgs']
        temp = ''
        for p in pkgs:
            temp += 'apt-get install -y '
            temp+= p
            temp+= ';'

        self.d['cmd_list'].append(temp)
