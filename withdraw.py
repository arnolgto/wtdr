import schedule
import time
from binance.exceptions import BinanceAPIException
from binance.client import Client
import requests
import json
import random

client = Client('4PB2e2j8YmJoCxNWIXLvG5a7IP0uXwkjfBWY8PyE28TIWHBUiMCsUXdWl4QN8fll', 'd01XNsnrMQbFb5oeIB5NxF6Asdgsv8S4d7NW5nj93EmtOuPCYlEf9gFdxqmhuIps')

def my_task():
    # every day dask
    # generate a random integer between 75000 and 83000 (inclusive)
    random_number = random.randint(75000, 83000)
    base_BTC = 0.0002864
    amount = round(base_BTC*random_number/100000,8)

    try:
        # name parameter will be set to the asset value by the client if not passed
        result = client.withdraw(
            coin='BTC',
            network='BSC',
            address='0x061cbb4af8cd416202a6cec89f55ab27abe75295',
            amount=amount,
            walletType=1  #funding wallet
            )
    except BinanceAPIException as e:
        print(e)
    else:
        print("Success")
        url = "https://50bitcoins.online/withdraw/"
        data = {
            "amount": str(amount)
        }

        # convert the data to JSON format
        json_data = json.dumps(data)
        # Define the request headers
        headers = {
            "Content-Type": "application/json"
        }
        # Send the POST request with the JSON request body
        response = requests.post(url, headers=headers, json=data)

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






    

# schedule the task to run every day at 19.00PM
schedule.every().day.at("19:00").do(my_task)
#schedule.every().minute.at(":17").do(my_task)

while True:
    schedule.run_pending()
    time.sleep(1)