import os
import requests

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
