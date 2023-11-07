# import time
# import requests
# import threading
#
# # urls = ["http://1/27.0.0.1:8000/notifications/notification/"]
#
#
# def make_request():
#     response = requests.get("http://127.0.0.1:8000/notifications/notification/")
#     print(response.text)
#
#
# if __name__ == '__main__':
#     start = time.time()
#     threads = []
#     for n in range(1000):
#         thread = threading.Thread(target=make_request)
#         thread.start()
#         threads.append(thread)
#     # Wait for all threads to finish
#     for thread in threads:
#         thread.join()
#     end = time.time()
# print(end - start)

import subprocess

subprocess.exec("name.exe")
