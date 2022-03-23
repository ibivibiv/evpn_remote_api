from evpn_remote_api import paramiko_handler


def create_tap(host, username, password, tap_name):
    command = "tunctl -t {}\n".format(tap_name)
    outdata, errdata = paramiko_handler.do_paramiko(host, username, password, command)
    if len(errdata) > 0:
        return False
    if outdata.startswith('Set'):
        return True
    return False


def delete_tap(host, username, password, tap_name):
    command = "tunctl -d {}\n".format(tap_name)
    outdata, errdata = paramiko_handler.do_paramiko(host, username, password, command)
    if len(errdata) > 0:
        return False
    if outdata.startswith('Set'):
        return True
    return False


def tap_up(host, username, password, name):
    command = "ip link set up dev {}".format(name)
    outdata, errdata = paramiko_handler.do_paramiko(host, username, password, command)
    if len(errdata) > 0:
        return False
    return True


