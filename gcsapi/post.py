import time

import requests
import json

start_time = time.time()
url = "http://127.0.0.1:8000/notifications/notification/"

for i in range(1000):
    payload = json.dumps({
        "username": [
            "admin@gmail.com"
        ],
        "password": [
            "admin@123"
        ]
    })

    response = requests.request("GET", url, data=payload)

    print(response.text)

print(time.time() - start_time)  # Result was: 9.66666889191


