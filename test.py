import schedule
import time
from binance.exceptions import BinanceAPIException
from binance.client import Client
import requests
import json
import random
import datetime
import os

# Reading the value of an environment variable
API = os.getenv('API')
SECRET = os.getenv('SECRET')
ADDRESS = os.getenv('ADDRESS')
URL = os.getenv('URL')

print('API: ',API)
print('SECRET: ',SECRET)
print('ADDRESS: ',ADDRESS)
print('URL: ',URL)


# every day dask
def my_task():
    # Get the current time of the server
    now = datetime.datetime.now()

    # Format the time using strftime() function
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")   
    
    # generate a random integer between 75000 and 83000 (inclusive)
    random_number = random.randint(75000, 83000)
    
    base_BTC = 0.0002864
    amount = round(base_BTC*random_number/100000,8)
    print('trying: ',amount)
    
    data = {
        "amount": str(amount),
        "servidor": formatted_time
    }

    # convert the data to JSON format
    json_data = json.dumps(data)
    # Define the request headers
    headers = {
        "Content-Type": "application/json"
    }
    # Send the POST request with the JSON request body
    response = requests.post(URL, headers=headers, json=data)

    #print(response.text)


    # check the response status code
    if response.status_code == 200:
        print("POST request was successful!")
        print("depósito: ", amount)
    else:
        print("POST request failed with status code", response.status_code)
        # check for any error messages returned in the response
        if "error" in response.json():
            print("Error:", response.json()["error"])
        else:
            print("No errors detected.")


# schedule the task to run every minute
schedule.every().minute.at(":17").do(my_task)

while True:
    schedule.run_pending()
    time.sleep(1)
