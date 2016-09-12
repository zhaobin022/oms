# -*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

import os

from ipip import IP
from ipip import IPX

IP.load(os.path.abspath("tinyipdata_utf8.dat"))
print IP.find("116.30.77.81")

