import iperf3


#set parameters
server_ip = 127.0.0.1
server_port = 5201
test_duration = 10


#Client options
client = iperf3.Client()
client.server_hostname = remote_site

