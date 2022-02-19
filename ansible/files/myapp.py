#!/usr/bin/env python3

import socket
import sys
import requests

def get_zk_stats(server, port=2181):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
      remote_ip = socket.gethostbyname(server)
      s.connect((remote_ip , port))
      request = b"stats\r\n"
      s.sendall(request)
      return s.recv(4096).decode("utf-8")
    except:
      return f"Connection to {server} failed.\r\n"

# get monitoring data for zookeeper (data in HA)
with open('/var/www/html/zk.txt','w') as zk_file:
  for srv in ['zoo-1', 'zoo-2', 'zoo-3']:
      zk_file.write(f"### {srv}\r\n")
      zk_file.write(get_zk_stats(srv))

# get load metrics directly from prometheus
with open('/var/www/html/load.txt','w') as load_file:
    res = requests.get('http://prometheus:9090/prometheus/api/v1/query', params={'query': 'node_load5'}).json()
    load_file.write(str(res['data']['result'])+"\r\n")

# get nginx stats
with open('/var/www/html/nginx.txt','w') as load_file:
  for srv in ['nginx-cdn', 'nginx-backend']:
      res = requests.get(f'http://{srv}/status').text
      load_file.write(f"### {srv}\r\n")
      load_file.write(str(res)+"\r\n")

