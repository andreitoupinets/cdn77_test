# Preparation

Put your SSH public key into `docker/.ssh/authorized_keys`. Check that your system have available ports in ranges 2211-2217 and 8880, 8881.
`docker-compose` creates internal subnet 172.16.238.0/24 for containers, it shouldn't overlap with existing docker networks. 

# Installation

Please go to `docker/` directory and run `docker-compose up --build`. 

After successfull start of all containers (based on debian with `sshd` in background), change directory to `ansible/`,
and run as first playbook `wireguard-infra.yml` - it prepares internal VPN network with separated subnet `10.255.13.0/24`.

Next playbook should be `monitoring.yml` - setup node-exporter for all containers,
it also install node-exporter to all nodes, setup on prometheus node prometheus server, grafana and alertmanager.
All others playbooks can be deployed in random order, but of course, monitoring app - `myapp` is depend on all other services.
For zookeeper playbook I use slightly modified external role with command `sleighzy.zookeeper`, it start/restart zookeeper without systemd service.


# Web Endpoints

 * http://localhost:8880/prometheus/
 * http://localhost:8880/grafana/
 * http://localhost:8880/alertmanager/
 * http://localhost:8880/myapp/zk.txt
   monitoring stats from zookeeper
 * http://localhost:8880/myapp/load.txt
   load stats, copied directly from prometheus API
 * http://localhost:8880/myapp/nginx.txt
   stats from stub nginx module, whole /myapp is cached for 30m on nginx-cdn container (experiment)


# TODO

* Grafana don't use datasource via wireguard vpn, because of complication with ansible facts.
* Iptables don't block traffic between hosts in subnet 172.16.238.0/24.
