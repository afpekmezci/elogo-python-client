
def get_array_of_string_type(client, list_ofstring):
    arr = client.get_type('arr:ArrayOfstring')
    return arr(list_ofstring)

