from netmiko import ConnectHandler
import concurrent.futures
import re

ip_address_file = input('Enter name of file for host addresses: ').strip()
t1 = time.perf_counter()

def fetch_ip_addresses():
    with open(ip_address_file) as devices:
        addresses = devices.read().splitlines()
    return addresses

def banner_rtr_configuration(address):

    ios_device_info = {
        'ip': address,
        'port': 8181,
        'username': 'admin',
        'password': 'Admin_1234!',
        'device_type': 'cisco_ios',
        'verbose': True
    }

    session = ConnectHandler(**ios_device_info)
    session.enable()

    cmds = ["config","banner motd \n Welcome to the DevNet Always On Sandbox for Open NX-OS \n  This is a shared sandbox available for anyone to use to \n test APIs, explore features, and test scripts.  Please \n keep this in mind as you use it, and respect others use. \n The following programmability features are already enabled: \n   - NX-API \n   - NETCONF, RESTCONF, gRPC \n   - Native NX-OS and OpenConfig YANG Models \n Thanks for stopping by and enjoy exploring the Open NX-OS","commit","exit","show banner motd"]
    session_return = session.send_config_set(cmds)
    file = (address + 'session_return.txt', 'w')
    file.write(session_return)
    file.close()
    session.disconnect()

with concurrent.futures.ThreadPoolExecutor() as exe:
    ip_addresses = fetch_ip_addresses()
    results = exe.map(banner_rtr_configuration, ip_addresses)

t2 = time.perf_counter()
print(f'The script finished executing in {round(t2-t1,2)} seconds.')
