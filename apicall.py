from ipaddress import IPv4Address
import uuid
import random
import copy
import pandas as pd
from pprint import pp
from pymongo import MongoClient
import requests
import json
import datetime
client = MongoClient('mongodb://localhost:27017/')

# select the database and collection
db = client['major']
collection = db['data']

random_ips = []

for _ in range(100):
    random_ips.append(str(IPv4Address(random.getrandbits(32))))

connected_nodes = copy.deepcopy(random_ips)

nodes = []
node_ids = []

##############################
# Randomly Generate 50 nodes #
##############################

for _ in range(100):
    node = {}
    addr = random.choice(random_ips)
    random_ips.remove(addr)

    id = str(uuid.uuid4())
    node_ids.append(id)
    node["id"] = id
    node["port"] = random.randint(20000, 40000)
    node["addr"] = addr
    node_connections = random.sample(connected_nodes, k=5)

    while addr in node_connections:
        node_connections = random.sample(connected_nodes, k=5)

    node["peers"] = node_connections

    is_node_good = random.choices([True, False], weights=(0.9, 0.1))[0]
    node["honest"] = "true" if is_node_good else "false"

    nodes.append(node)

#pp(nodes)

messages = []

#################################
# Randomly generate 50 messages #
#################################

for _ in range(100):
    message = {}
    start_date = datetime.date(2022, 9, 1)
    end_date = datetime.date(2023, 1,31)

    start_time = datetime.time(0, 0, 0)
    end_time = datetime.time(23, 59, 59)

    random_date = datetime.date.fromordinal(random.randint(start_date.toordinal(), end_date.toordinal()))
    random_time = datetime.time(random.randint(start_time.hour, end_time.hour),
                                random.randint(start_time.minute, end_time.minute),
                                random.randint(start_time.second, end_time.second))
    date=datetime.datetime.combine(random_date, random_time)
    unix_timestamp= date.strftime('%Y-%m-%d %H:%M:%S')
    sender_receiver = random.sample(node_ids, k=2)
    message["sender"] = sender_receiver[0]
    message["receiver"] = sender_receiver[1]
    message["date"] = unix_timestamp
    message["payload"] = {
        "temperature": random.randint(20, 30),
        "wind": random.randint(0, 16),
        "speed": random.randint(100, 200),
    }
    messages.append(message)

#pp(messages)

for item in messages:
    # convert the dictionary to a string and replace single quotes with double quotes
    json_string = str(item).replace("'", "\"")
    json_string = json.loads(json_string)
    response = requests.post('http://127.0.0.1:8050/store', json=json_string)
for ite in nodes:
    # convert the dictionary to a string and replace single quotes with double quotes
    json_strin = str(ite).replace("'", "\"")
    json_strin = json.loads(json_strin)
    response = requests.post('http://127.0.0.1:8050/store', json=json_strin)


