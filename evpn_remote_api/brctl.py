from evpn_remote_api import paramiko_handler


def create_bridge(host, username, password, bridge_name):
    command = "brctl addbr {}\n".format(bridge_name)
    outdata, errdata = paramiko_handler.do_paramiko(host, username, password, command)
    if len(errdata) > 0:
        return False
    return True


def delete_bridge(host, username, password, bridge_name):
    command = "brctl delbr {}\n".format(bridge_name)
    outdata, errdata = paramiko_handler.do_paramiko(host, username, password, command)
    if len(errdata) > 0:
        return False
    return True


def addif_bridge(host, username, password, bridge_name, if_name):
    command = "brctl addif {} {}".format(bridge_name, if_name)
    outdata, errdata = paramiko_handler.do_paramiko(host, username, password, command)
    if len(errdata) > 0:
        return False
    return True


def delif_bridge(host, username, password, bridge_name, if_name):
    command = "brctl delif {} {}".format(bridge_name, if_name)
    outdata, errdata = paramiko_handler.do_paramiko(host, username, password, command)
    if len(errdata) > 0:
        return False
    return True


def bridge_up(host, username, password, bridge_name):
    command = "ip link set up dev {}".format(bridge_name)
    outdata, errdata = paramiko_handler.do_paramiko(host, username, password, command)
    if len(errdata) > 0:
        return False
    return True


# results = create_bridge('192.168.0.96', 'root', 'hal2000', 'br400')
# results = delete_bridge('192.168.0.96', 'root', 'hal2000', 'br400')
results = addif_bridge('192.168.0.96', 'root', 'hal2000', 'br400', "vxlan200")
print(results)
