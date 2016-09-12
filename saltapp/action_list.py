__author__ = 'zhaobin022'

from saltapp.modules import cmd
from saltapp.modules import state


module_dic = {
    'cmd' : cmd.Cmd,
    'state': state.State
}