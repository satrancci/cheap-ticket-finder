import os
import requests
from collections import defaultdict

def get_nordvpn_servers():
    r = requests.get("https://nordvpn.com/api/server")
    servers = r.json()
    return servers

# filters out all non-standard VPN servers
def parse_nordvpn_servers(servers):
    f = lambda y: any(list(map(lambda x: "Standard VPN servers" in x["name"], y["categories"] )))
    standard_vpn_servers = list(map(lambda x: x["domain"], list(filter( f, servers ))))
    return standard_vpn_servers

def store_nordvpn_servers(servers):
    dir_to_store = "nordvpn_servers"
    if not dir_to_store in os.listdir():
        os.mkdir(dir_to_store)
    with open(f"{dir_to_store}/servers.txt", "w") as f:
        for server in servers:
            server_name = server.split('.')[0]
            f.write(server_name)
            f.write('\n')

def process_nordvpn_servers():
    servers = get_nordvpn_servers()
    standard_vpn_servers = parse_nordvpn_servers(servers)
    store_nordvpn_servers(standard_vpn_servers)

def store_servers_for_each_country():
    dir = "nordvpn_servers"
    d = defaultdict(list)
    with open(f"{dir}/servers.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            line = line.strip()
            country_code, server_code = line[:2], line[2:]
            d[country_code].append(server_code)
    
    for country_code, server_codes in d.items():
        with open(f"{dir}/{country_code}.txt", "w") as f:
            for server_code in server_codes:
                full_code = country_code+server_code
                f.write(full_code)
                f.write('\n')
    