import uuid

#def my_random_string(string_length=10):
def my_random_string():
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    #random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    #return random[0:string_length] # Return the random string.
    return random

#print(my_random_string(10))
print(my_random_string())