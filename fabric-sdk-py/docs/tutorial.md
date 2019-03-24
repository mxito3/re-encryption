# Tutorial of Using Fabric Python SDK

**Note: The tutorial is still in-progress, and the full version example code can be found at [sample.py](sample.py).**

**Note: Python3 is required.**

TLDR, run a quick example testing.

```bash
$ HLF_VERSION=1.4.0
$ docker pull hyperledger/fabric-peer:${HLF_VERSION}
$ docker pull hyperledger/fabric-orderer:${HLF_VERSION}
$ docker pull hyperledger/fabric-ca:${HLF_VERSION}
$ docker pull hyperledger/fabric-ccenv:${HLF_VERSION}
$ docker-compose -f test/fixtures/docker-compose-2orgs-4peers-tls.yaml up
$ pip3 install virtualenv; make venv
$ source venv/bin/activate
$ make install
$ python docs/sample.py
$ deactive
```

## 0. Prepare a Testing Environment

### 0.1. Install Fabric SDK

```bash
$ git clone https://github.com/hyperledger/fabric-sdk-py.git
$ cd fabric-sdk-py
$ make install
```

Optionally, you can also verify the version number or run all testing cases.

```bash
$ python
>>> import hfc
>>> print(hfc.VERSION)
0.7.0
>>> exit()

$ make check
```

### 0.2. Setup a Fabric Network

If you already have a running fabric network, ignore this.

To start an example fabric network you can simply run the following command:

```bash
$ HLF_VERSION=1.4.0
$ docker pull hyperledger/fabric-peer:${HLF_VERSION}
$ docker pull hyperledger/fabric-orderer:${HLF_VERSION}
$ docker pull hyperledger/fabric-ca:${HLF_VERSION}
$ docker pull hyperledger/fabric-ccenv:${HLF_VERSION}
$ docker-compose -f test/fixtures/docker-compose-2orgs-4peers-tls.yaml up
```

Then you'll have a fabric network with 3 organizations, 4 peers and 1 orderer:
 * org1.example.com
   * peer0.org1.example.com
   * peer1.org1.example.com
 * org2.example.com
   * peer0.org2.example.com
   * peer1.org2.example.com
 * orderer.example.com
   * orderer.example.com

* Note: make sure `configtxgen` is in the '$PATH'.

If you want to understand more details on starting up a fabric network, feel free to see the [Building Your First Network](https://hyperledger-fabric.readthedocs.io/en/latest/build_network.html) tutorial.

### 0.3. Create the Connection Profile

A network connection profile helps SDK connect to the fabric network by providing all required information to operate with a fabric network, including:

* Client credentials file location;
* Service endpoints for peer, orderer and ca;

The [network.json](test/fixtures/network.json) is an example, please modify the content accordingly.

Now you can use the Python SDK to work with the fabric network!

## 1. Get Credentials

### 1.1 Load the Connection Profile

Load all network information from the profile, and check the resources.

```python
from hfc.fabric import Client

cli = Client(net_profile="test/fixtures/network.json")

print(cli.organizations)  # orgs in the network
print(cli.peers)  # peers in the network
print(cli.orderers)  # orderers in the network
print(cli.CAs)  # ca nodes in the network, TODO
```

### 1.2 Prepare User Id (Optionally)

SDK need the credential file as a valid network user.

Typically there are two ways: using cryptogen or using Fabric-CA. That will depend on how your network boots up with.

#### 1.2.1 Using Local Credential

SDK will load the valid credential from local path (the credentail files must be put there in advance).

```python
from hfc.fabric import Client

cli = Client(net_profile="test/fixtures/network.json")
org1_admin = cli.get_user(org_name='org1.example.com', name='Admin') # get the admin user from local path
```

#### 1.2.2 Get Credentail from Fabric CA

Here demos how to interact with Fabric CA.

* Enroll into Fabric CA with admin role;
* Register a user `user1`;
* Enroll with the new user `user1` and get local credential;
* Re-enroll the `user1`;
* Revoke the `user1`.

```python
from hfc.fabric_ca.caservice import ca_service

cli = ca_service(target="https://127.0.0.1:7054")
adminEnrollment = cli.enroll("admin", "pass") # now local will have the admin enrollment
secret = adminEnrollment.register("user1") # register a user to ca
user1Enrollment = cli.enroll("user1", secret) # now local will have the user enrollment
user1ReEnrollment = cli.reenroll(user1Enrollment) # now local will have the user reenrolled object
RevokedCerts, CRL = adminEnrollment.revoke("user1") # revoke the user if you need
```

You can also use the new identity management system:

```python
from hfc.fabric_ca.caservice import ca_service

cacli = ca_service(target="https://127.0.0.1:7054")
identityService = cacli.newIdentityService()

admin = cacli.enroll("admin", "pass") # now local will have the admin user
secret = identityService.create(admin, 'foo') # create user foo
res = identityService.getOne('foo', admin) # get user foo
res = identityService.getAll(admin) # get all users
res = identityService.update('foo', admin, maxEnrollments=3, affiliation='.', enrollmentSecret='bar') # update user foo
res = identityService.delete('foo', admin) # delete user foo
```

## 2. Operate Channels with Fabric Network


### 2.1 Create a new channel and join it

Use sdk to create a new channel and let peers join it.

```python
from hfc.fabric import Client

cli = Client(net_profile="test/fixtures/network.json")
org1_admin = cli.get_user(org_name='org1.example.com', name='Admin')

# Create a New Channel, the response should be true if succeed
response = cli.channel_create(
            orderer_name='orderer.example.com',
            channel_name='businesschannel',
            requestor=org1_admin,
            config_yaml='test/fixtures/e2e_cli/',
            channel_profile='TwoOrgsChannel'
            )
print(response==True)

# Join Peers into Channel, the response should be true if succeed
response = cli.channel_join(
               requestor=org1_admin,
               channel_name='businesschannel',
               peer_names=['peer0.org1.example.com',
                           'peer1.org1.example.com']
               orderer_name='orderer.example.com'
               )
print(response==True)


# Join Peers from a different MSP into Channel
org2_admin = cli.get_user(org_name='org2.example.com', name='Admin')

# For operations on peers from org2.example.com, org2_admin is required as requestor
response = cli.channel_join(
               requestor=org2_admin,
               channel_name='businesschannel',
               peer_names=['peer0.org2.example.com',
                           'peer1.org2.example.com']
               orderer_name='orderer.example.com'
               )
print(response==True)
```

### 2.2 Update the Channel Configuration

TBD. [Help on this](https://jira.hyperledger.org/browse/FABP-199).

## 3. Operate Chaincodes with Fabric Network

Use sdk to install, instantiate and invoke chaincode.

```python
from hfc.fabric import Client

cli = Client(net_profile="test/fixtures/network.json")
org1_admin = cli.get_user('org1.example.com', 'Admin')

# Install Example Chaincode to Peers
# GOPATH setting is only needed to use the example chaincode inside sdk
import os
gopath_bak = os.environ.get('GOPATH', '')
gopath = os.path.normpath(os.path.join(
                      os.path.dirname(os.path.realpath('__file__')),
                      'test/fixtures/chaincode'
                     ))
os.environ['GOPATH'] = os.path.abspath(gopath)

# The response should be true if succeed
response = cli.chaincode_install(
               requestor=org1_admin,
               peer_names=['peer0.org1.example.com',
                           'peer1.org1.example.com']
               cc_path='github.com/example_cc',
               cc_name='example_cc',
               cc_version='v1.0'
               )

# Instantiate Chaincode in Channel, the response should be true if succeed
args = ['a', '200', 'b', '300']
response = cli.chaincode_instantiate(
               requestor=org1_admin,
               channel_name='businesschannel',
               peer_names=['peer0.org1.example.com'],
               args=args,
               cc_name='example_cc',
               cc_version='v1.0'
               )

# Invoke a chaincode
args = ['a', 'b', '100']
# The response should be true if succeed
response = cli.chaincode_invoke(
               requestor=org1_admin,
               channel_name='businesschannel',
               peer_names=['peer0.org1.example.com'],
               args=args,
               cc_name='example_cc',
               cc_version='v1.0'
               )

# Query a chaincode
args = ['b']
# The response should be true if succeed
response = cli.chaincode_query(
               requestor=org1_admin,
               channel_name='businesschannel',
               peer_names=['peer0.org1.example.com'],
               args=args,
               cc_name='example_cc',
               cc_version='v1.0'
               )
```

## 4. Query Informations

By default, `query` methods returns a decoded response.

If you need to get the raw response from the ledger you can add `decode=False` param.

### 4.1 Basic Usage

```python
from hfc.fabric import Client

cli = Client(net_profile="test/fixtures/network.json")
org1_admin = cli.get_user('org1.example.com', 'Admin')

# Query Peer installed chaincodes, make sure the chaincode is installed
response = cli.query_installed_chaincodes(
               requestor=org1_admin,
               peer_names=['peer0.org1.example.com'],
               decode=True
               )

"""
# An example response:

chaincodes {
  name: "example_cc"
  version: "1.0"
  path: "github.com/example_cc"
}
"""

# Query Peer Joined channel
response = cli.query_channels(
               requestor=org1_admin,
               peer_names=['peer0.org1.example.com'],
               decode=True
               )

"""
# An example response:

channels {
  channel_id: "businesschannel"
}
"""

# Query Channel Info
response = cli.query_info(
               requestor=org1_admin,
               channel_name='businesschannel',
               peer_names=['peer0.org1.example.com'],
               decode=True
               )

# Query Block by tx id
# example txid of instantiated chaincode transaction
response = cli.query_block_by_txid(
               requestor=org1_admin,
               channel_name='businesschannel',
               peer_names=['peer0.org1.example.com'],
               tx_id=cli.txid_for_test,
               decode=True
               )
```

### 4.2 Query Block by block hash

```python
from hfc.fabric import Client

cli = Client(net_profile="test/fixtures/network.json")
org1_admin = cli.get_user('org1.example.com', 'Admin')

# first get the hash by calling 'query_info'
response = cli.query_info(
               requestor=org1_admin,
               channel_name='businesschannel',
               peer_names=['peer0.org1.example.com'],
               decode=True
               )

test_hash = response.currentBlockHash

response = cli.query_block_by_hash(
               requestor=org1_admin,
               channel_name='businesschannel',
               peer_names=['peer0.org1.example.com'],
               block_hash=test_hash,
               decode=True
               )
```

### 4.3 Query Block, Transaction and Instantiated Chaincodes

```python
from hfc.fabric import Client

cli = Client(net_profile="test/fixtures/network.json")
org1_admin = cli.get_user('org1.example.com', 'Admin')

# Query Block by block number
response = cli.query_block(
               requestor=org1_admin,
               channel_name='businesschannel',
               peer_names=['peer0.org1.example.com'],
               block_number='1',
               decode=True
               )

# Query Transaction by tx id
# example txid of instantiated chaincode transaction
response = cli.query_transaction(
               requestor=org1_admin,
               channel_name='businesschannel',
               peer_names=['peer0.org1.example.com'],
               tx_id=cli.txid_for_test,
               decode=True
               )

# Query Instantiated Chaincodes
response = cli.query_instantiated_chaincodes(
               requestor=org1_admin,
               channel_name='businesschannel',
               peer_names=['peer0.org1.example.com'],
               decode=True
               )
```

### 4.4 Get channel configuration

```python
from hfc.fabric import Client

cli = Client(net_profile="test/fixtures/network.json")
org1_admin = cli.get_user('org1.example.com', 'Admin')

# Get channel config
response = cli.get_channel_config(
               requestor=org1_admin,
               channel_name='businesschannel',
               peer_names=['peer0.org1.example.com'],
               decode=True
               )
```

## License <a name="license"></a>

<a rel="license" href="http://creativecommons.org/licenses/by/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by/4.0/88x31.png" /></a><br />This document is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International License</a>.
