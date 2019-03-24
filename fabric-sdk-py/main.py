from hfc.fabric import Client

cli = Client(net_profile="test/fixtures/network.json")

print(cli.organizations)  # orgs in the network
print(cli.peers)  # peers in the network
print(cli.orderers)  # orderers in the network
print(cli.CAs)  # ca nodes in the network, TODO