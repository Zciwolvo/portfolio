from flask import Flask, request, jsonify, Blueprint
import json
from datetime import datetime
import re
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from pymongo.server_api import ServerApi

from scraper import scrapping


uri = "mongodb+srv://skapiec.4ju5ocq.mongodb.net/?authSource=%24external&authMechanism=MONGODB-X509&retryWrites=true&w=majority&appName=Skapiec"
certificate_file = '/home/IgorGawlowicz/mysite/static/certs/X509-cert-3621885173140152299.pem'

# Connect to MongoDB
client = MongoClient(uri, tls=True, tlsCertificateKeyFile=certificate_file, server_api=ServerApi('1'), connectTimeoutMS=30000, socketTimeoutMS=None, connect=False, maxPoolsize=1)
db = client.get_database("Skapiec")

skapiec_blueprint = Blueprint("skapiec", __name__)
# Enable CORS for all routes of the Flask skapiec_blueprint
CORS(skapiec_blueprint)

# Define the path to the JSON file
JSON_PATH = "/home/IgorGawlowicz/mysite/static/data/skapiec_data.json"

# Function to read data from a JSON file
def read_json_file(file_path):
    # Open the JSON file in read mode and load the data into a Python dictionary
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data

# Function to write data to a JSON file
def write_json_file(file_path, data):
    # Open the JSON file in write mode and dump the data to the file
    # with UTF-8 encoding, ensuring special characters are handled properly
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

# Function to find the index of an item with a specific URL in a list of dictionaries
def find_index(data, url):
    # Iterate through the list of dictionaries and find the index of the dictionary
    # with the 'internal_url' matching the provided URL
    for i, item in enumerate(data):
        if item['internal_url'] == url:
            return i

def read_from_mongodb(collection_name):
    # Get the collection
    collection = db[collection_name]
    # Query all documents from the collection excluding the _id field
    documents = collection.find({}, {'_id': 0})
    # Convert documents to JSON
    json_data = [doc for doc in documents]
    return json_data


def write_to_mongodb(collection_name, json_data):
    # Get the collection
    db[collection_name].delete_many({})
    collection = db[collection_name]
    # Insert JSON data into the collection
    collection.insert_many(json_data)

# Function to extract a money value from a string
def extract_money_value(money_string):
    # Define a regular expression pattern to match numbers with or without decimals
    pattern = r'\d+(\.\d+)?'
    # Search for a match in the input string using the regular expression pattern
    match = re.search(pattern, money_string)
    if match:
        # If a match is found, convert it to a float and return the value
        return float(match.group())
    else:
        # If no match is found, return None
        return None


# localhost:5000/scrape?phrase=rower
@skapiec_blueprint.route('/skapiec/scrape', methods=['GET'])  # Define a route '/scrape' accessible via GET method
def scrape():
    phrase = request.args.get('phrase')  # Get the value of the 'phrase' query parameter from the request
    pages = request.args.get('pages')

    if not pages:
        pages = 1

    if phrase:  # Check if the 'phrase' parameter is provided
        result = scrapping(phrase, pages)  # Call the scrapping function with the provided phrase
        data = read_from_mongodb("skapiec")  # Read existing data from the JSON file
        current_datetime = datetime.now()


        # Iterate through the items in the result
        for item in result:
            # Check if any item with the same 'internal_url' exists in the data
            try:
                check = any(x['internal_url'] == item['internal_url'] for x in data)
            except KeyError:
                check = False
            if check:
                # If item exists, find its index in the data list
                index_of_item = find_index(data, item['internal_url'])

                # Extract new and old prices from the item and existing data
                price_new = extract_money_value(item['price'])
                price_old = extract_money_value(data[index_of_item]['price_lowest'])

                # Compare new price with old lowest price
                if price_new <= price_old:
                    # If new price is lower or equal, update lowest price and timestamps
                    data[index_of_item]['price_lowest'] = item['price']
                    data[index_of_item]['price'] = item['price']
                    data[index_of_item]['update_lowest'] = current_datetime.strftime('%Y.%m.%d %H:%M')
                    data[index_of_item]['update'] = current_datetime.strftime('%Y.%m.%d %H:%M')
                else:
                    # If new price is higher, update price and timestamp
                    data[index_of_item]['price'] = item['price']
                    data[index_of_item]['update'] = current_datetime.strftime('%Y.%m.%d %H:%M')
            else:
                # If item doesn't exist in data, create a new data_item dictionary
                data_item = {
                    'id': len(data)+1,  # Generate a unique ID for the item
                    'search': phrase,  # Store the search phrase
                    'name': item['name'],  # Store the item name
                    'price': item['price'],  # Store the item price
                    'price_lowest': item['price'],  # Store the item lowest price
                    'external_url': item['external_url'],  # Store the external URL
                    'internal_url': item['internal_url'],  # Store the internal URL
                    'photo': item['photo'],  # Store the item photo
                    'update': current_datetime.strftime('%Y.%m.%d %H:%M'),  # Store the current timestamp as update time
                    'update_lowest': current_datetime.strftime('%Y.%m.%d %H:%M')  # Store the current timestamp as update lowest time
                }
                # Append the new data_item to the data list
                data.append(data_item)

        # Write the updated data back to the JSON file
        write_to_mongodb("skapiec", data)
        return 'Data saved to JSON file'  # Return success message
    else:
        return 'Missing phrase parameter', 400  # Return error message if 'phrase' parameter is missing

# http://localhost:5000/get_data?phrase=rower
@skapiec_blueprint.route('/skapiec/get_data', methods=['GET'])  # Define a route '/get_data' accessible via GET method
def get_data():
    phrase = request.args.get('phrase')  # Get the value of the 'phrase' query parameter from the request

    data = read_from_mongodb("skapiec") # Read existing data from the JSON file

    # Filter the data to include only records where the 'search' field matches the provided phrase
    if phrase:
        filtered_data = [record for record in data if record.get('search') == phrase]

        # Return the filtered data as a JSON response
        return jsonify(filtered_data)
    else:
        return jsonify(data)

if __name__ == '__main__':
    skapiec_blueprint.run(debug=True)
