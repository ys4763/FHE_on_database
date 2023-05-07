from phe import paillier
import csv
import pickle
import time

start_time = time.time()
public_key, private_key = paillier.generate_paillier_keypair()

# Save keys to file
with open('paillier_keys.pkl', 'wb') as f:
    pickle.dump((public_key, private_key), f)

# Load keys from file
#with open('paillier_keys.pkl', 'rb') as f:
#    public_key, private_key = pickle.load(f)

with open('output.csv', newline='') as csvfile:
    reader = csv.reader(csvfile)
    header = next(reader) # Get header row

    # Encrypt remaining rows using Paillier encryption
    counter = 0
    encrypted_rows = []
    for row in reader:
        # set the r_value to 1, so that the cipher text won't be obfustrated with a random number
        encrypted_row = [public_key.encrypt(int(cell), r_value = 1) for cell in row]
        encrypted_rows.append(encrypted_row)
        
        counter += 1
        if counter % 5 == 0:
            print(f"{counter} rows processed")
        #if counter == 30:
        #    break
    #print(encrypted_rows)

print("encrypting done...")

# Save encrypted data to a file
with open('encrypted_data.pkl', 'wb') as f:
    pickle.dump((header, encrypted_rows), f)

end_time = time.time()
running_time = end_time - start_time
print(f"Program finished in {running_time:.2f} seconds")



'''
# Convert the dataset into a suitable format for encryption
with open('output.csv', mode='r') as file:
    reader = csv.reader(file)#, delimiter = ';')
    dataset = []
    for row in reader:
        secret_number_list = []
        for num in row:
            secret_number_list.append(int(num))
        print(secret_number_list)
        #encrypted_number_list = [public_key.encrypt(x) for x in secret_number_list]
        #dataset.append(encrypted_number_list)
    print(dataset)
'''