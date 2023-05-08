import socket as so
from phe import paillier
import pickle
import time

# Load data from file
with open('encrypted_data.pkl', 'rb') as f:
    header, encrypted_rows = pickle.load(f)
    
def average(column_index):
    # Extract the encrypted cells from the chosen column
    encrypted_column = [encrypted_row[column_index] for encrypted_row in encrypted_rows]

    # Compute the sum of the encrypted cells
    encrypted_sum = encrypted_column[0]
    for i in range(1, len(encrypted_column)):
        encrypted_sum += encrypted_column[i]

    # Compute the average by dividing the sum by the number of rows
    n_rows = len(encrypted_rows)
    encrypted_average = encrypted_sum * (1 / n_rows)
    
    return encrypted_average
    
# 2. Number of dataset entries matching a given keyword
def count(column_index, target):
    # initialize the count variable
    count = 0
    # iterate over the rows and count the matches
    for row in encrypted_rows:
        if row[column_index].ciphertext(False) == target.ciphertext(False):
            count += 1
    
    return count    
    

# 3. Position (within dataset) of dataset entries matching a given keyword
def find_positions(column_index, target):
    # initialize the count variable
    position_list = []
    # iterate over the rows and count the matches
    for index, row in enumerate(encrypted_rows):
        if row[column_index].ciphertext(False) == target.ciphertext(False):
            position_list.append(index)
    return position_list

# 4. All dataset entries matching multiple given keywords
def filter_dataset(condition_columns):
    position_list = []
    # Filter the dataset based on the conditions
    for index, row in enumerate(encrypted_rows):
        # Check if the row satisfies all conditions
        satisfied = True
        for column_index, condition_value in condition_columns:
            if row[column_index].ciphertext(False) != condition_value.ciphertext(False):
                satisfied = False
                break
        if satisfied:
            position_list.append(index)
    return position_list
    

# create socket
server_socket = so.socket(so.AF_INET, so.SOCK_STREAM)

# work locally
host = '127.0.0.1'
port = 9999

# bind to localhost and a port
server_socket.bind((host, port))

server_socket.listen()

while True:
	# establish conenction
	client_socket, address = server_socket.accept()
	q1 = ""
	q2 = ""
	q3 = ""
	
	print("Got a connection from {}".format(address))
	
	# Greetings prompt 1
	p1 = "Hello Alice, what do you want to learn about your database?\n"
	p1 += "Choose from the following:\n"
	p1 += "1. The average of one attribute\n"
	p1 += "2. The number of entries matching your given value\n"
	p1 += "3. The positions of entries matching your given value\n"
	p1 += "4. All the entries matching your given value\n"
	p1 += "Enter \"Goodbye\" to close the connection\n"
	
	client_socket.send(p1.encode('ascii'))
	
	# Query part 1
	q1 = client_socket.recv(1024).decode()
	if q1 == "Goodbye":
		# close
		client_socket.close()
	else:
		# second prompt
		p2 = "Which attribute are you interested in learning?\n"
		p2 += "Choose from the following:\n"
		p2 += "1. Age; 2. Mother's Education; 3. Father's Education; 4. Home from School travel time;\n"
		p2 += "5. Weekly study time; 6. Number of failure; 7. Quality of family relationship;\n"
		p2 += "8. Free time after school; 9. Go out with friends; 10. Workday alcohol consumption;\n"
		p2 += "11. Weekend alcohol consumption; 12. Current health status; \n"
		p2 += "13. First period grade; 14. Second period grade; 15. Thrid period grade.\n"
		p2 += "Enter \"Goodbye\" to close the connection\n"
		if int(q1) != 4:
			client_socket.send(p2.encode('ascii'))
		else:
		    p2 += "Please enter your conditions in the format of\n"
		    p2 += "Column_number1,Value1;Column_number2,Value2;..."
		    client_socket.send(p2.encode('ascii'))
		    q2 = client_socket.recv(8196)
		    # print(q2)
		    conditions = pickle.loads(q2)
		    res = filter_dataset(conditions)
		    result = pickle.dumps(res)
		    client_socket.sendall(result)
		    continue
		
		# Query part 2
		q2 = client_socket.recv(4096).decode()
		if q2 == "Goodbye":
			client_socket.close()
		if int(q1) == 1:
			column = int(q2) - 1
			avg = pickle.dumps(average(column))
			client_socket.sendall(avg)
		else:
			# third prompt
			p3 = "Please specify your value: "
			client_socket.send(p3.encode('ascii'))
			q3 = client_socket.recv(4096)
			val = pickle.loads(q3)
			column = int(q2) - 1
			if int(q1) == 2:
			    res = count(column, val)
			if int(q1) == 3:
			    res = find_positions(column, val)
			send = pickle.dumps(res)
			client_socket.sendall(send)
	client_socket.close()
