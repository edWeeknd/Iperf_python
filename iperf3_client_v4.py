#Initializing server in Daemon mode and save log in normal format:
#iperf3 -s -D --logfile /home/student/AAA_Work/Server_output/server1.txt



import iperf3
import sys
import time
import os
from datadog import initialize, statsd

# Datadog API Key
api_key = '864801d4951e3cad9a71f94637358009'

# Set DD options for statsd init
options = {
    'statsd_host': '127.0.0.1',
    'statsd_port': 8125,
    'api_key': api_key
}
initialize(**options)

#set parameters
server_ip = '127.0.0.1'
server_port = 5201
test_duration = 30 #in s
num_stream = 5
bandwidth = 10 #in Mbps 
protocol = "tcp"


#Client set-up
def client_run():
	client = iperf3.Client()
	client.server_hostname = server_ip
	client.zerocopy = True
	client.verbose = False
	client.reverse = True
	client.port = server_port
	client.num_streams = num_stream
	client.duration = int(test_duration)
	client.bandwidth = bandwidth*1024**2
	client.protocol = protocol
	client.blksize = 32000

	#Run iperf3 client
	result = client.run()

	return result


#Output handling
def output_print(result):
	#Connection summary
	# print(full_path)
	print("------------------------BEGIN OUTPUT------------------------------------------\n")
	print("Connection summary:")
	print(result.time)
	print("Client: "+str(result.local_host))
	print("Server: "+str(result.remote_host)+":"+str(result.remote_port))
	print("Protocol: "+result.protocol)
	print("Reverse direction: "+str(result.reverse))
	print("Number of test streams: "+str(result.num_streams))
	print("Test duration: "+str(result.duration)+" s")
	print("\n------------------------------------------------------------------------------\n")

	#Extract data for TCP
	if result.protocol == "TCP":
		print("Total sent bitrate: "+str(round(result.sent_Mbps,2))+" Mbps")
		print("Total received bitrate: "+str(round(result.received_Mbps,2))+" Mbps")
		print("Data sent: "+str(round(result.sent_bytes/(1024**2),2))+" MBytes")
		print("Data received: "+str(round(result.received_bytes/(1024**2),2))+" MBytes")
		print("Retransmits: "+str(result.retransmits))
	#Extract data for UDP	
	else:
		print("Total bitrate: "+str(round(result.Mbps,2))+" Mbps")
		print("Data transmitted: "+str(round(result.bytes/(1024**2),2))+" MBytes")
		print("Jitter: "+str(round(result.jitter_ms,3))+" ms")
		print("Packet lost: "+str(result.lost_packets)+"/"+str(result.packets)+" ("+str(result.lost_percent)+"%)")
	
	print("\n------------------------END OUTPUT--------------------------------------------")


def output_json(result):
	#Get path to Output directory
	absolute_path = os.path.dirname(__file__)
	relative_path = "Client_output"
	full_path = os.path.join(absolute_path, relative_path)

	#Get time stampt for log file's name
	timestr = time.strftime("%Y%m%d-%H%M%S")
	filename = f"json_{timestr}"

	with open(f'{full_path}/{filename}.txt', 'a') as f:
		sys.stdout = f
		print(result.text)



def output_2_file(result):
	#Get path to Output directory
	absolute_path = os.path.dirname(__file__)
	relative_path = "Client_output"
	full_path = os.path.join(absolute_path, relative_path)

	#Get time stampt for log file's name
	timestr = time.strftime("%Y%m%d-%H%M%S")
	filename = f"log_{timestr}"

	with open(f'{full_path}/{filename}.txt', 'a') as f:
		sys.stdout = f
		output_print(result)



def main():
	result = client_run()
	output_print(result)
	output_2_file(result)
	output_json(result)

	sent_mbps = int(result.sent_Mbps)
	received_mbps = int(result.received_Mbps)
	# send Metrics to DD and add some tags for classification in DD GUI
	# send bandwidth metric - egress mbps
	statsd.gauge('iperf3.test.mbps.egress', sent_mbps, tags=["team_name:my_team", "team_app:iperf"])
	# send bandwidth metric - ingress mbps
	statsd.gauge('iperf3.test.mbps.ingress', received_mbps, tags=["team_name:my_team", "team_app:iperf"])


if __name__ == "__main__":
	main()





#Output handling
# #Get path to Output directory
# absolute_path = os.path.dirname(__file__)
# relative_path = "Output"
# full_path = os.path.join(absolute_path, relative_path)

# #Get time stampt for log file's name
# timestr = time.strftime("%Y%m%d-%H%M%S")
# filename = f"log_{timestr}"

# with open(f'{full_path}/{filename}.txt', 'a') as f:
# 	sys.stdout = f
# 	#Connection summary
# 	# print(full_path)
# 	print("------------------------BEGIN OUTPUT------------------------------------------")
# 	print("Connection summary:")
# 	print(result.time)
# 	print("Client: "+str(result.local_host)+":"+str(result.local_port))
# 	print("Server: "+str(result.remote_host)+":"+str(result.remote_port))
# 	print("Protocol: "+result.protocol)
# 	print("Reverse direction: "+str(result.reverse))
# 	print("Number of test streams: "+str(result.num_streams))
# 	print("\n------------------------------------------------------------------------------\n")

# 	#Extract data
# 	print("Total sent bitrate: "+str(round(result.sent_Mbps,2))+" Mbps")
# 	print("Total received bitrate: "+str(round(result.received_Mbps,2))+" Mbps")
# 	print("Data sent: "+str(round(result.sent_bytes/(1024**2),2))+" MBytes")
# 	print("Data received: "+str(round(result.received_bytes/(1024**2),2))+" MBytes")
# 	print("------------------------END OUTPUT--------------------------------------------")