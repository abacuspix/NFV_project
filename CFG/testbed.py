from fabric.api import env

#Management ip addresses of hosts in the cluster
host1 = 'root@17.1.1.231'
host2 = 'root@17.1.1.232'
host3 = 'root@17.1.1.233'
host4 = 'root@17.1.1.234'
host5 = 'root@17.1.1.235'

#External routers if any
#for eg. 
#ext_routers = [('mx1', '10.204.216.253')]
ext_routers = []

#Autonomous system number
router_asn = 64512

#Host from which the fab commands are triggered to install and provision
host_build = 'root@17.1.1.231'

#Role definition of the hosts.
env.roledefs = {
    'all': [host1, host2, host3, host4, host5],
    'cfgm': [host1,host2,host3],
    'openstack': [host1,host2,host3],
    'control': [host2, host3],
    'compute': [host4, host5],
    'collector': [host1,host2,host3],
    'webui': [host1,host2,host3],
    'database': [host1,host2,host3],
    'build': [host_build],
}

env.hostnames = {
    'all': ['openstack', 'control-1', 'control-2', 'compute-1', 'compute-2']
}

#Openstack admin password
env.openstack_admin_password = 'root123'

env.password = 'root123'
#Passwords of each host
env.passwords = {
    host1: 'root123',
    host2: 'root123',
    host3: 'root123',
    host4: 'root123',
    host5: 'root123',
    host_build: 'root123',
}

#For reimage purpose
env.ostypes = {
    host1: 'ubuntu',
    host2: 'ubuntu',
    host3: 'ubuntu',
    host4: 'ubuntu',
    host5: 'ubuntu',
}
minimum_diskGB = 256
env.interface_rename = False

env.ha = {
    'internal_vip'   : '1.1.1.100',
    'external_vip'   : '17.1.1.230',
}

do_parallel = True



control_data = {
    host1 : { 'ip': '1.1.1.1/24', 'gw' : '1.1.1.254', 'device':'eth1' },
    host2 : { 'ip': '1.1.1.2/24', 'gw' : '1.1.1.254', 'device':'eth1' },
    host3 : { 'ip': '1.1.1.3/24', 'gw' : '1.1.1.254', 'device':'eth1' },
    host4 : { 'ip': '4.4.4.4/24', 'gw' : '4.4.4.254', 'device':'eth1' },
    host5 : { 'ip': '5.5.5.5/24', 'gw' : '5.5.5.254', 'device':'eth1' },
}

static_route  = {
    host1 : [{ 'ip': '4.4.4.0', 'netmask' : '255.255.255.0', 'gw':'1.1.1.254', 'intf': 'eth1' },
             { 'ip': '5.5.5.0', 'netmask' : '255.255.255.0', 'gw':'1.1.1.254', 'intf': 'eth1' }],
    host2 : [{ 'ip': '4.4.4.0', 'netmask' : '255.255.255.0', 'gw':'1.1.1.254', 'intf': 'eth1' },
             { 'ip': '5.5.5.0', 'netmask' : '255.255.255.0', 'gw':'1.1.1.254', 'intf': 'eth1' }],
    host3 : [{ 'ip': '4.4.4.0', 'netmask' : '255.255.255.0', 'gw':'1.1.1.254', 'intf': 'eth1' },
             { 'ip': '5.5.5.0', 'netmask' : '255.255.255.0', 'gw':'1.1.1.254', 'intf': 'eth1' }],
    host4 : [{ 'ip': '1.1.1.0', 'netmask' : '255.255.255.0', 'gw':'4.4.4.254', 'intf': 'eth1' },
             { 'ip': '5.5.5.0', 'netmask' : '255.255.255.0', 'gw':'4.4.4.254', 'intf': 'eth1' }],
    host5 : [{ 'ip': '1.1.1.0', 'netmask' : '255.255.255.0', 'gw':'5.5.5.254', 'intf': 'eth1' },
             { 'ip': '4.4.4.0', 'netmask' : '255.255.255.0', 'gw':'5.5.5.254', 'intf': 'eth1' }],
}


