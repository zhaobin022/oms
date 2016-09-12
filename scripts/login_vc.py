__author__ = 'zhaobin022'
import ssl

from pyVim.connect import SmartConnect, Disconnect
from pyVmomi import vim, vmodl
#import requests

context = None

# Disabling urllib3 ssl warnings
#requests.packages.urllib3.disable_warnings()

# Disabling SSL certificate verification
if hasattr(ssl, 'SSLContext'):
    context = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
    context.verify_mode = ssl.CERT_NONE

vc = None

vcenter_host = "192.168.26.8"
vcenter_port = 443
vcenter_username = "administrator@vsphere.local"
vcenter_password = "Sun65Ape$"

# Connecting to vCenter
try:
    if context:
        vc = SmartConnect(host=vcenter_host, user=vcenter_username, pwd=vcenter_password, port=vcenter_port, sslContext=context)
    else:
        vc = SmartConnect(host=vcenter_host, user=vcenter_username, pwd=vcenter_password, port=vcenter_port)

except IOError as e:
    print "I/O error({0}): {1}".format(e.errno, e.strerror)