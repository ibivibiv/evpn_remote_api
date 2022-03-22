import time
import paramiko


def do_paramiko(host, username, password, command):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=username, password=password)
    print('Successfully connected to %s' % host)

    sleeptime = 0.001
    outdata, errdata = '', ''
    ssh_transp = ssh.get_transport()
    chan = ssh_transp.open_session()
    # chan.settimeout(3 * 60 * 60)
    chan.setblocking(0)
    chan.exec_command(command)
    while True:  # monitoring process
        # Reading from output streams
        while chan.recv_ready():
            outdata += chan.recv(1000).decode('UTF-8')
        while chan.recv_stderr_ready():
            errdata += chan.recv_stderr(1000).decode('UTF-8')
        if chan.exit_status_ready():  # If completed
            break
        time.sleep(sleeptime)
    retcode = chan.recv_exit_status()
    ssh_transp.close()
    return outdata, errdata
