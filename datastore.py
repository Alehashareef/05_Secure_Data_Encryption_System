# In-memory data storage (dictionary)
stored_data = {}

# Function to add encrypted data to the storage
def add_data(username, encrypted_text, hashed_passkey):
    stored_data[username] = {"encrypted_text": encrypted_text, "passkey": hashed_passkey}

# Function to retrieve stored data
def get_data(username):
    return stored_data.get(username)
