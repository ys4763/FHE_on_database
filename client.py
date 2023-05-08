import socket as so
from phe import paillier
import pickle
import time

# Load keys from file
with open('paillier_keys.pkl', 'rb') as f:
    public_key, private_key = pickle.load(f)

# Create socket
client_socket = so.socket(so.AF_INET, so.SOCK_STREAM)

# local host
host = '127.0.0.1'
port = 9999

# connect to the local host on the port
client_socket.connect((host, port))

count = 0
query = 0
while True:
	# receive message from server
	message = client_socket.recv(1024)

	# decode and print
	print(message.decode('ascii'))
	
	# send reply
	reply = input()
	# print(reply)
	if count <= 1 and query != "1" and query != "4":
	    client_socket.send(reply.encode())
	if reply == "Goodbye":
		break
	else:
	    count += 1
	if count == 1:
	    query = reply
	elif count == 2 and query == "1":
	    answer = client_socket.recv(4096)
	    answer = pickle.loads(answer)
	    output = private_key.decrypt(answer)
	    print("The average is {}".format(output))
	    break
	elif count == 2 and query == "4":
	    #print(reply)
	    conditions = []
	    condition = reply.split(";")
	    for c in condition:
	        each = c.split(",")
	        conditions.append([int(each[0])-1, public_key.encrypt(int(each[1]), r_value=1)])
	    send = pickle.dumps(conditions)
	    print(pickle.loads(send))
	    client_socket.send(send)
	    res = client_socket.recv(8196)
	    res = pickle.loads(res)
	    print("There position of students satisfying all of the query values are {}".format(res))
	elif count == 3:
	    val = int(reply.strip())
	    value = public_key.encrypt(val, r_value=1)
	    send = pickle.dumps(value)
	    #print(pickle.loads(send))
	    client_socket.send(send)
	    res = client_socket.recv(4096)
	    res = pickle.loads(res)
	    if int(query == "2"):
	        print("There are {} students satisfying your value".format(res))
	        break
	    else:
	        print("There position of students satisfying the query value are {}".format(res))
	        break
client_socket.close()
