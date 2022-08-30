import requests


baseURL = "http://ponyia.ddns.net:8080/api/v1/"


data = requests.get(baseURL+'user/getAllUser')
print(data.text)