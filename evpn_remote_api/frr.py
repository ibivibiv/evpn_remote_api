from evpn_remote_api import paramiko_handler

def create_bgp_router(host, username, password, asn, router_id, route_reflectors):
    rr_command = []
    for route_reflector in route_reflectors:
        cmd = "-c 'neighbor {} peer-group fabric'".format(route_reflector)
        rr_command.append(cmd)
    string_rr_list = " ".join(rr_command)
    command = "vtysh -c 'configure terminal' -c 'router bgp {}' -c 'bgp router-id {}' -c 'no bgp default ipv4-unicast' -c 'neighbor fabric peer-group' -c 'neighbor fabric remote-as {}' -c 'neighbor fabric capability extended-nexthop' {} -c 'neighbor fabric activate' -c 'advertise-all-vni' -c 'exit-address-family' -c 'do write'".format(
        asn, router_id, asn, string_rr_list)
    outdata, errdata = paramiko_handler.do_paramiko(host, username, password, command)
    if len(errdata) > 0:
        return False
    if "[OK]" in outdata :
        return True
    return False


def create_bgp_reflector(host, username, password, asn, router_id, subnet):
    command = "vtysh -c 'configure terminal' -c 'router bgp {}' -c 'bgp router-id {}' -c 'bgp cluster-id {}' -c 'no bgp default ipv4-unicast' -c 'neighbor fabric peer-group' -c 'neighbor fabric remote-as {}' -c 'neighbor fabric capability extended-nexthop' -c 'neighbor fabric update-source {}' -c 'bgp listen range {} peer-group fabric' -c 'address-family l2vpn evpn' -c 'neighbor fabric activate' -c 'neighbor fabric route-reflector-client' -c 'exit-address-family' -c 'do write'".format(
        asn, router_id, router_id, asn, router_id, subnet)
    outdata, errdata = paramiko_handler.do_paramiko(host, username, password, command)
    if len(errdata) > 0:
        return False
    if "[OK]" in outdata :
        return True
    return False

def get_bgp_router_id(host, username, password) :
    command = "vtysh -c 'show bgp attribute-info'"
    outdata, errdata = paramiko_handler.do_paramiko(host, username, password, command)
    if len(errdata) > 0:
        return False
    parts = outdata.split()
    for i in range(len(parts)) :
        if "nexthop" in parts[i] :
            id = parts[i+1]
            return id
    return False
