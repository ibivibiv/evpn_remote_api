from evpn_remote_api import paramiko_handler


def list_evpn(host, username, password):
    command = "vtysh -c 'show evpn vni'\n"
    outdata, errdata = paramiko_handler.do_paramiko(host, username, password, command)
    if len(errdata) > 0:
        return {"error": errdata}
    l = outdata.split('\n')
    results = []
    for line in l[1:]:
        evpn = {}
        fixed = line.split()
        if len(fixed) > 0:
            evpn['vni'] = fixed[0]
            evpn['type'] = fixed[1]
            evpn['interface'] = fixed[2]
            evpn['macs'] = fixed[3]
            evpn['arps'] = fixed[4]
            evpn['remote_vteps'] = fixed[5]
            evpn['tenant_vrf'] = fixed[6]
            results.append(evpn)

    return results


def create_evpn_vni_interface(host, username, password, name, vni, dstport, local_tunnel_ip):
    command = "ip link add {} type vxlan id {} dstport {} local {} nolearning".format(name, vni, dstport,
                                                                                      local_tunnel_ip)
    outdata, errdata = paramiko_handler.do_paramiko(host, username, password, command)
    if len(errdata) > 0:
        return False
    return True


def delete_evpn_vni_interface(host, username, password, name):
    command = "ip link del {}".format(name)
    outdata, errdata = paramiko_handler.do_paramiko(host, username, password, command)
    if len(errdata) > 0:
        return False
    return True


def evpn_up(host, username, password, name):
    command = "ip link set up dev {}".format(name)
    outdata, errdata = paramiko_handler.do_paramiko(host, username, password, command)
    if len(errdata) > 0:
        return False
    return True


