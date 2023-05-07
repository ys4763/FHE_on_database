from phe import paillier
import pickle
import time

# Load keys from file
with open('paillier_keys.pkl', 'rb') as f:
    public_key, private_key = pickle.load(f)

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

    # Decrypt the average using the private key
    decrypted_average = private_key.decrypt(encrypted_average)

    print(f'The average of column {column_index} is: {decrypted_average}')


# 2. Number of dataset entries matching a given keyword
def count(column_index, target):
    # initialize the count variable
    count = 0
    # iterate over the rows and count the matches
    for row in encrypted_rows:
        if row[column_index].ciphertext(False) == target.ciphertext(False):
            count += 1

    # encrypt the count (should we encrypt the count while transferring?)
    #encrypted_count = public_key.encrypt(count)
    
    # following part might should be in Client side
    print("There are " + str(count) + " students whose " + header[column_index] + " is...") # the plaintext of the target should only be known to Client


# 3. Position (within dataset) of dataset entries matching a given keyword
def find_positions(column_index, target):
    # initialize the count variable
    position_list = []
    # iterate over the rows and count the matches
    for index, row in enumerate(encrypted_rows):
        if row[column_index].ciphertext(False) == target.ciphertext(False):
            position_list.append(index)

    # encrypt the count (should we encrypt the count while transferring?)
    #encrypted_count = public_key.encrypt(count)
    
    # following part might should be in Client side
    print("Target found at positions: ", position_list)


# 4. All dataset entries matching a given keyword
def filter_dataset(condition_columns):
    filtered_data = []
    counter = 0
    # Filter the dataset based on the conditions
    for row in encrypted_rows:
        # Check if the row satisfies all conditions
        satisfied = True
        for column_index, condition_value in condition_columns:
            if row[column_index].ciphertext(False) != condition_value.ciphertext(False):
                satisfied = False
                break
        if satisfied:
            filtered_data.append(row)
            counter += 1

    # Decrypt the filtered dataset
    decrypted_filtered_data = []
    for row in filtered_data:
        decrypted_row = [private_key.decrypt(x) for x in row]
        decrypted_filtered_data.append(decrypted_row)
    print(f'We found {counter} matches:')
    print(header)
    print(decrypted_filtered_data)




if __name__ == "__main__":    
    # 1. calculate the average of a column
    average(0)

    # 2. Number of dataset entries matching a given keyword
    # following should be done in client side
    encrypted_number = public_key.encrypt(16, r_value = 1)

    count(0, encrypted_number)

    # 3. Position (within dataset) of dataset entries matching a given keyword
    # following should be done in client side
    encrypted_number = public_key.encrypt(16, r_value = 1)

    find_positions(0, encrypted_number)


    # 4. All dataset entries matching a given keyword
    # client side, find the columns and encrypt its keywords
    # "conditions" is a list containing all conditions, the format is [[column1, keyword1], [column2, keyword2], ...]
    conditions = [[0, public_key.encrypt(18, r_value = 1)], [3, public_key.encrypt(2, r_value = 1)]]
    filter_dataset(conditions)