import iperf3
import sys
import time
import os



#set log file

#set parameters
server_ip = '127.0.0.1'
server_port = 5201
test_duration = 2 #in s
num_stream = 4 
bandwidth = 10 #in Mbps 

#Client set-up
client = iperf3.Client()
client.server_hostname = server_ip
client.zerocopy = True
client.verbose = False
client.reverse = False
client.port = server_port
client.num_streams = num_stream
client.duration = int(test_duration)
client.bandwidth = bandwidth*1024**2
# client.json_output = False


#Run iperf3 client
result = client.run()


#Output handling
def output_print():
	#Connection summary
	# print(full_path)
	print("------------------------BEGIN OUTPUT------------------------------------------")
	print("Connection summary:")
	print(result.time)
	print("Client: "+str(result.local_host)+":"+str(result.local_port))
	print("Server: "+str(result.remote_host)+":"+str(result.remote_port))
	print("Protocol: "+result.protocol)
	print("Reverse direction: "+str(result.reverse))
	print("Number of test streams: "+str(result.num_streams))
	print("\n------------------------------------------------------------------------------\n")

	#Extract data
	print("Total sent bitrate: "+str(round(result.sent_Mbps,2))+" Mbps")
	print("Total received bitrate: "+str(round(result.received_Mbps,2))+" Mbps")
	print("Data sent: "+str(round(result.sent_bytes/(1024**2),2))+" MBytes")
	print("Data received: "+str(round(result.received_bytes/(1024**2),2))+" MBytes")
	print("------------------------END OUTPUT--------------------------------------------")


def output_2_file():
	#Get path to Output directory
	absolute_path = os.path.dirname(__file__)
	relative_path = "Output"
	full_path = os.path.join(absolute_path, relative_path)

	#Get time stampt for log file's name
	timestr = time.strftime("%Y%m%d-%H%M%S")
	filename = f"log_{timestr}"

	with open(f'{full_path}/{filename}.txt', 'a') as f:
		sys.stdout = f
		output_print()

output_print()
output_2_file()

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