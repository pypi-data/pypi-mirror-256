# Python Blockchain Package
---
jupyter:
  colab:
    collapsed_sections:
    - 4a2Ss7ivGiHF
    toc_visible: true
  kernelspec:
    display_name: Python 3
    name: python3
  language_info:
    name: python
  nbformat: 4
  nbformat_minor: 0
---

::: {.cell .markdown id="6tqzm-XLGbtu"}
<https://www.tutorialspoint.com/python_blockchain/python_blockchain_quick_guide.htm>
:::

::: {.cell .markdown id="4a2Ss7ivGiHF"}
# Import Libraries
:::

::: {.cell .code execution_count="1" id="2VJFK5B4Zzi_"}
``` python
# import libraries
import hashlib
import random
import string
import json
import binascii
import numpy as np
import pandas as pd
import pylab as pl
import logging
import datetime
import collections
```
:::

::: {.cell .code execution_count="2" colab="{\"base_uri\":\"https://localhost:8080/\"}" id="X3b5PrToX1cm" outputId="b1eb0566-65f0-40d8-e328-b966c79f1e82"}
``` python
!pip install pycryptodome
```

::: {.output .stream .stdout}
    Requirement already satisfied: pycryptodome in /usr/local/lib/python3.10/dist-packages (3.20.0)
:::
:::

::: {.cell .code execution_count="3" id="dASWKPDYXnCu"}
``` python
# following imports are required by PKI
import Crypto
import Crypto.Random
from Crypto.Hash import SHA
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
```
:::

::: {.cell .markdown id="Lpsj_8GMHXcZ"}
# Function / Class Definition {#function--class-definition}
:::

::: {.cell .markdown id="c9Y8Pu0zGrn0"}
## Client
:::

::: {.cell .code execution_count="4" id="p3X2m1jmXpm9"}
``` python
class Client:
  def __init__(self):
    random = Crypto.Random.new().read
    self._private_key = RSA.generate(1024, random)
    self._public_key = self._private_key.publickey()
    self._signer = PKCS1_v1_5.new(self._private_key)

  @property
  def identity(self):
    return binascii.hexlify(self._public_key.exportKey(format='DER')).decode('ascii')
```
:::

::: {.cell .markdown id="pbJIybaIHDnT"}
## Transaction
:::

::: {.cell .code execution_count="5" id="Hddz3q75Y-kY"}
``` python
class Transaction:
  def __init__(self, sender, recipient, value):
    self.sender = sender
    self.recipient = recipient
    self.value = value
    self.time = datetime.datetime.now()

  def to_dict(self):
    if self.sender == "Genesis":
      identity = "Genesis"
    else:
      identity = self.sender.identity

    return collections.OrderedDict({
      'sender': identity,
      'recipient': self.recipient,
      'value': self.value,
      'time' : self.time})

  def sign_transaction(self):
    private_key = self.sender._private_key
    signer = PKCS1_v1_5.new(private_key)
    h = SHA.new(str(self.to_dict()).encode('utf8'))
    return binascii.hexlify(signer.sign(h)).decode('ascii')
```
:::

::: {.cell .code execution_count="6" id="KPu0OFvwZtzZ"}
``` python
def display_transaction(transaction):
  dict = transaction.to_dict()
  print("sender: " + dict['sender'])
  print('-----')
  print("recipient: " + dict['recipient'])
  print('-----')
  print("value: " + str(dict['value']))
  print('-----')
  print("time: " + str(dict['time']))
  print('-----')
```
:::

::: {.cell .markdown id="gOjFyyq1HICS"}
## Block
:::

::: {.cell .code execution_count="7" id="W9w7PvSRbdfm"}
``` python
class Block:
  def __init__(self):
    self.verified_transactions = []
    self.previous_block_hash = ""
    self.Nonce = ""
```
:::

::: {.cell .code execution_count="8" id="kI-2Lh7Lcbnq"}
``` python
def dump_blockchain(self):
  print("Number of blocks in the chain: " + str(len(self)))
  for x in range(len(self)):
    block_temp = self[x]
    print("block # " + str(x))
    for transaction in block_temp.verified_transactions:
      display_transaction(transaction)
      print('--------------')
    print('=====================================')
```
:::

::: {.cell .markdown id="IVWY0zw0HLu0"}
## Miner
:::

::: {.cell .code execution_count="9" id="qqgHh6sHdFL2"}
``` python
def sha256(message):
  return hashlib.sha256(message.encode('ascii')).hexdigest()
```
:::

::: {.cell .code execution_count="10" id="S7NocbN2dFOI"}
``` python
def mine(message, difficulty=1):
  assert difficulty >= 1
  prefix = '1' * difficulty
  for i in range(1000):
    digest = sha256(str(hash(message)) + str(i))
    if digest.startswith(prefix):
      print ("after " + str(i) + " iterations found nonce: "+ digest)
      return digest
```
:::

::: {.cell .markdown id="Po9VBB-6HlXK"}
# Sample Run
:::

::: {.cell .code execution_count="11" id="tCriBsLjcblU"}
``` python
sample_chain = []
```
:::

::: {.cell .code execution_count="12" id="ijI7qxH9Zt31"}
``` python
clientA = Client()
clientB = Client()
clientC = Client()
clientD = Client()
```
:::

::: {.cell .code execution_count="13" id="fZ5ugC-zbdmD"}
``` python
t0 = Transaction("Genesis", clientA.identity, "GENESIS")

block0 = Block()
block0.previous_block_hash = None
block0.verified_transactions.append(t0)

digest = hash(block0)
last_block_hash = digest

sample_chain.append(block0)
```
:::

::: {.cell .code execution_count="14" id="5nO1RHs9Y-3I"}
``` python
transactions = []

t1 = Transaction(clientA, clientB.identity, "Hello world!")
t1.sign_transaction()
transactions.append(t1)

t2 = Transaction(clientB, clientC.identity, "Testing123")
t2.sign_transaction()
transactions.append(t2)

t3 = Transaction(clientC, clientD.identity, "QWERTY")
t3.sign_transaction()
transactions.append(t3)
```
:::

::: {.cell .code execution_count="15" colab="{\"base_uri\":\"https://localhost:8080/\"}" id="T84YsMYLA2GU" outputId="f8b4ed04-dfab-4514-a8eb-cc9ffebb2edf"}
``` python
last_transaction_index = 0

block = Block()
for i in range(3):
  temp_transaction = transactions[last_transaction_index]
  # validate transaction
  # if valid
  block.verified_transactions.append(temp_transaction)
  last_transaction_index += 1

block.previous_block_hash = last_block_hash
block.Nonce = mine(block, 2)
digest = hash(block)
sample_chain.append(block)
last_block_hash = digest
```

::: {.output .stream .stdout}
    after 74 iterations found nonce: 11f1bd0d400e1f3e15c28678125505a10ac2a2887612199b4542e90d11279081
:::
:::

::: {.cell .code execution_count="16" colab="{\"base_uri\":\"https://localhost:8080/\"}" id="cuVJK14fb0xX" outputId="1f1ba5a4-bea6-4560-b5c6-238090f31577"}
``` python
dump_blockchain(sample_chain)
```

::: {.output .stream .stdout}
    Number of blocks in the chain: 2
    block # 0
    sender: Genesis
    -----
    recipient: 30819f300d06092a864886f70d010101050003818d0030818902818100ba2ca0d2e55da37535496ab3ba8050e5040385a4e773b6ec51f3f7ef507db39783a69e45c8a24ef2e612e4e5c992dfebf013490d79578cd4ec731e16cc60231501253c138a0a762c67c6dd5196e27dc70d18226b89d407cadd199e2362defc349ecdd95bc6132dd9ca022369eaea0fe3911a3727dea83c215804e51da65dae410203010001
    -----
    value: GENESIS
    -----
    time: 2024-02-15 09:44:41.419833
    -----
    --------------
    =====================================
    block # 1
    sender: 30819f300d06092a864886f70d010101050003818d0030818902818100ba2ca0d2e55da37535496ab3ba8050e5040385a4e773b6ec51f3f7ef507db39783a69e45c8a24ef2e612e4e5c992dfebf013490d79578cd4ec731e16cc60231501253c138a0a762c67c6dd5196e27dc70d18226b89d407cadd199e2362defc349ecdd95bc6132dd9ca022369eaea0fe3911a3727dea83c215804e51da65dae410203010001
    -----
    recipient: 30819f300d06092a864886f70d010101050003818d0030818902818100d9c28c710023dc06d0861764011b4b2e8dbff935ab165ccc392cf7ad88aa0a37782cd0c7efd94f20adf50190dedf6d9948725d6f206a67e846d06e595b6216d4712d56a340753efd615fa4fb7e0304b7f9f19b232b12f9245f437993620ba84a1a62e04f4e3837ba913dcc4db7e1b55cabb258ba32762f4ae201846e048a7df50203010001
    -----
    value: Hello world!
    -----
    time: 2024-02-15 09:44:41.440960
    -----
    --------------
    sender: 30819f300d06092a864886f70d010101050003818d0030818902818100d9c28c710023dc06d0861764011b4b2e8dbff935ab165ccc392cf7ad88aa0a37782cd0c7efd94f20adf50190dedf6d9948725d6f206a67e846d06e595b6216d4712d56a340753efd615fa4fb7e0304b7f9f19b232b12f9245f437993620ba84a1a62e04f4e3837ba913dcc4db7e1b55cabb258ba32762f4ae201846e048a7df50203010001
    -----
    recipient: 30819f300d06092a864886f70d010101050003818d00308189028181009c4d5ae58fef5373d61e5237a3b7348113d34807fab37cfa3453ec93dc9317089eb8f8d23c32b0f65742676702414350eee3fe14e30d5961922b3a85b6dde472a2b06be17ad61c7a517e94eb60199d826ef9e0aee748eef93ed25e98d48ddb15b226c05086674566826b2afb9402e4f5736f96ce2f3b7b27b7502cf1914cbe450203010001
    -----
    value: Testing123
    -----
    time: 2024-02-15 09:44:41.454331
    -----
    --------------
    sender: 30819f300d06092a864886f70d010101050003818d00308189028181009c4d5ae58fef5373d61e5237a3b7348113d34807fab37cfa3453ec93dc9317089eb8f8d23c32b0f65742676702414350eee3fe14e30d5961922b3a85b6dde472a2b06be17ad61c7a517e94eb60199d826ef9e0aee748eef93ed25e98d48ddb15b226c05086674566826b2afb9402e4f5736f96ce2f3b7b27b7502cf1914cbe450203010001
    -----
    recipient: 30819f300d06092a864886f70d010101050003818d0030818902818100a7f5f79c8c1184493bd63b7920cde72d1686d7017a480fa13099f961f20a42f1047c1547cd037cdd15144a1422e0a4dca120155849a9f808f48a6522613921d18835722ba1a3181e375e622ef926f81af49a0e5b5117320d59b8b4105f6eb3e9086db2523e16ae879dee65fc6afe386ba7f199ad5f7429294c6ff58fa62905370203010001
    -----
    value: QWERTY
    -----
    time: 2024-02-15 09:44:41.458706
    -----
    --------------
    =====================================
:::
:::
