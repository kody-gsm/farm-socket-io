import subprocess

def get_mac():
    strs = str(subprocess.check_output('ifconfig -a | grep ether | head -1', shell=True)).strip().split('ether')
    strs = strs[1].split(' ')[1].replace(':', '')
    print(strs)

get_mac()
