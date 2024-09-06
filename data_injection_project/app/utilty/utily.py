import hashlib
import os
import uuid
import json
import pandas as pd

# Function to read an Excel file and return a DataFrame
def read_excel_file(file_path):
    """
    Reads an Excel file and returns a DataFrame.
    """
    try:
        current_path = f"{os.getcwd()}/app/files/excel/{file_path}"
        df = pd.read_excel(current_path)

        return {"data": df}

    except Exception as err:
        print(f"Error while reading Excel file: {err}")
        return {
            "error": f"Error while reading Excel file for file name: {file_path}"
        }


def read_json_file(file_path):
    """
    Reads a JSON file and returns data.
    """
    try:
        current_path = f"{os.getcwd()}/app/files/json_file/{file_path}"
        with open(current_path, 'r') as f:
            data = json.load(f)

        return {"data": data}
    except Exception as err:
        print(f"Error while reading json file : {err}")
        return {
            "error": f"Error while reading json file for file name: {file_path}"
        }


def create_json_file(data, file_name):
    """
    Creates a JSON file from data.
    """
    try:
        current_path = f"{os.getcwd()}/app/project/movies/{file_name}"
        with open(current_path, 'w') as f:
            json.dump(data, f, indent=4)

        return {
            "data": file_name
        }

    except Exception as err:
        print(f"Error while creating json file: {err}")
        return {
            "error": f"Error while creating json file for file name: {file_name}"
        }


def create_uuid(uniquestring):
    """
    Creates a UUID from a given string.
    """
    try:
        namespace = uuid.NAMESPACE_DNS
        generated_uuid = uuid.uuid5(namespace, uniquestring)

        return {
            "data": generated_uuid
        }

    except Exception as err:
        print(f"Error while genrating UUID: {err}")
        return {
            "error": f"Error while genrating UUID for uniquestring : {uniquestring}"
        }


def string_to_7_digit_number(input_string):
    """
    Converts a string to a 7-digit number using SHA-256 hash.
    """

    try:
        hash_object = hashlib.sha256(input_string.encode())
        hex_dig = hash_object.hexdigest()
        hash_int = int(hex_dig, 16)
        seven_digit_number = (hash_int % 9000000) + 1000000

        return {
            "data": seven_digit_number
        }

    except Exception as err:
        print(f"Error while creating string to 7 digit number: {err}")
        return {
            "error": f"Error while creating string to 7 digit number for uniquestring : {input_string}"
        }


def add_value_to_key(key, sample_movie_data, title_type, data):
    """
    Appends short and long titles or descriptions to sample_movie_data.
    """
    try:

        for title_type_key in ["eng", "may", "tam", "chi", "tha", "ind"]:

            if key not in ["title", "description"]:
                sample_movie_data[key][title_type_key] = str(data).split(",")
            else:
                sample_movie_data[key][title_type][title_type_key] = data
        return {
            "data": True
        }
    except Exception as err:
        print(f"Error in the add_value_to_key function : {str(err)}")
        return {
            "error": data
        }


def append_genre(key, sample_movie_data, title_type, data):
    """
    Appends genre information to sample_movie_data.
    """
    try:
        for title_type_key in ["eng", "may", "tam", "chi", "tha", "ind"]:
            if title_type == "primary":
                data = data.split(",")[0]
            else:
                if len(data.split(",")) > 1:
                    data = data.split(",")[1]
                else:
                    data = data.split(",")[0]
            sample_movie_data[key][title_type][0]["name"][title_type_key] = data
        return {
            "data": True
        }
    except Exception as err:
        print(f"Error in the append_genre function : {str(err)}")
        return {
            "error": data
        }


def append_image(sample_movie_data, type, url):
    """
    Appends image URLs to sample_movie_data.
    """
    try:
       
        url = f"https://datastore.videoready.int.xp.irdeto.com/{url}"
        for item in sample_movie_data['images']:
            if item['type'] == type:
                item['url'] = url
            elif item['type'] == type:
                item['url'] = url
            elif item['type'] == type:
                item['url'] = url
        return {
            "data": True
        }
    except Exception as err:
        print(f"Error in the append_image function : {str(err)}")
        return {
            "error": url
        }
