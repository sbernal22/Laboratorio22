import requests
r = requests.get('https://httpbin.org/get')
data = r.json()
print(data["origin"])
print(data["headers"])
print(data["args"])
