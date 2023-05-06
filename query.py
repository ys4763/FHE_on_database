from phe import paillier
import pickle
import time

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

    # Decrypt the average using the private key
    decrypted_average = private_key.decrypt(encrypted_average)

    print(f'The average of column {column_index} is: {decrypted_average}')

def count(column_index, target):
    # initialize the count variable
    count = 0
    print(target)
    # iterate over the rows and count the matches
    for row in encrypted_rows:
        print(row[column_index].ciphertext(be_secure = False))
        if row[column_index].ciphertext(False) == target.ciphertext(False):
            count += 1
    print("the count is:" + str(count))

    # encrypt the count
    #public_key = private_key.public_key
    #encrypted_count = public_key.encrypt(count)

if __name__ == "__main__":
    # Load keys from file
    with open('paillier_keys.pkl', 'rb') as f:
        public_key, private_key = pickle.load(f)

    # Load data from file
    with open('encrypted_data.pkl', 'rb') as f:
        header, encrypted_rows = pickle.load(f)
    
    encrypted_number = public_key.encrypt(16)
    count(0, encrypted_number)
