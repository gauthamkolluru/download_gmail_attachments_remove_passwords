import json

FILE_NAME = "pdf_passwords.json"

def read_json(file_name=FILE_NAME, data=dict()) -> (str, list):

    with open(file_name) as fn:
        data = json.load(fn)

    return data['root_dir'], data['passwords']